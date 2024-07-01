import requests
import config
import urllib.parse
import math
import numpy as np

#Helper functions for formatting data to use with OR-Tools

def standard_to_minutes(time):
    time = time.split(':')
    hours = int(time[0])
    minutes = int(time[1])
    hours *= 60
    total_minutes = hours + minutes
    return total_minutes

#Returns necessary node information to model the problem
def create_node_mapping(edges, edge_los):
    node_data = {}
    #map duplicate nodes to their actual location
    node_to_index = {}
    # map nodes to their corresponding trip
    node_to_trip = {}
    #Record whether a node is a pick-up or drop-off
    node_to_demand_A = {} #Can be either 1, -1, or 0
    node_to_demand_W = {} #Can be either 1, -1, or 0
    #Depot has demand 0
    node_to_demand_A[0] = 0
    node_to_demand_W[0] = 0
    #Store new unique edge list
    new_edges = []
    #Keep track of indexes
    seen = set()
    for i, edge in enumerate(edges):
        #check for and process duplicate nodes
        new_edge = []
        if edge[0] not in seen:
            seen.add(edge[0])
            new_edge.append(edge[0])
        else:
            #len of seen plus 1 is the new index
            index = len(seen)+1
            seen.add(index)
            node_to_index[index] = edge[0]
            new_edge.append(index)
        if edge_los[i] == 'A' or edge_los[i] == 'ADD':
            node_to_demand_A[new_edge[-1]] = 1
            node_to_demand_W[new_edge[-1]] = 0
        else:
            node_to_demand_A[new_edge[-1]] = 0
            node_to_demand_W[new_edge[-1]] = 1
        if edge[1] not in seen:
            seen.add(edge[1])
            new_edge.append(edge[1])
        else:
            index = len(seen)+1
            seen.add(index)
            node_to_index[index] = edge[1]
            new_edge.append(index)
        if edge_los[i] == 'A' or edge_los[i] == 'ADD':
            node_to_demand_A[new_edge[-1]] = -1
            node_to_demand_W[new_edge[-1]] = 0
        else:
            node_to_demand_A[new_edge[-1]] = 0
            node_to_demand_W[new_edge[-1]] = -1
        new_edges.append(new_edge)
        node_to_trip[new_edge[0]] = i
        node_to_trip[new_edge[1]] = i
    node_data["new_edges"] = new_edges
    node_data["node_to_index"] = node_to_index
    #Add one to account for 0 index (depot)
    node_data["num_nodes"] = len(seen)+1
    node_data["node_to_demand_A"] = node_to_demand_A
    node_data["node_to_demand_W"] = node_to_demand_W
    node_data["node_to_trip"] = node_to_trip
    return node_data

def build_address_str(addresses):
    #Build a pipe seperated string of adresses
    address_str = ''
    for i in range(len(addresses)-1):
        address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

def send_request(origins, destinations):
    #Build and send API request
    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_address_str = build_address_str(origins)
    dest_address_str = build_address_str(destinations)
    API_key = config.API_KEY
    url = request + '&origins=' + origin_address_str + '&destinations=' + dest_address_str + '&key=' + API_key
    response = requests.get(url)
    return response.json()

def build_matrix(response, type):
    matrix = []
    if type == 'distance':
         for row in response['rows']:
            row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
            matrix.append(row_list)
    if type == 'time':
        for row in response['rows']:
            row_list = [math.ceil((row['elements'][j]['duration']['value'])/60) for j in range(len(row['elements']))]
            matrix.append(row_list)
    return matrix


#Creates a distance or time matrix with the given addresses
def create_matrix(addresses, type):
    #Check if this matrix has already been created and is in the cache
     if check_cache():
        matrix = get_cache()
        return matrix
     else:
        matrix = create_matrix_helper(addresses, type)
        save_cache(matrix)
        return matrix
     
def create_matrix_helper(addresses, type):
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    max_addresses = 25
    num_addresses = len(addresses)

    #Useful if addresses is > max_addresses
    q0, r0 = divmod(num_addresses, max_addresses)
    print(q0, r0)

    if num_addresses > max_addresses:
        num_addresses_per_request = max_addresses
    else:
        num_addresses_per_request = num_addresses

    #Now calculate the number of rows per request
    max_rows = max_elements // num_addresses_per_request
    q, r = divmod(num_addresses, max_rows) 
    print(q,r)
    dest_addresses = addresses
    matrix = []

    #Send q requests, returning max rows per request
    for i in range(q):
        print("Iteration: " + str(i))
        block = np.array([])
        origin_addresses = addresses[i * max_rows: (i+1) * max_rows]
        for j in range (q0):
            print("Inner loop: " + str(j))
            dest_addresses = addresses[j * num_addresses_per_request: (j+1) * num_addresses_per_request]
            print("Dest: " + str(len(dest_addresses)))
            print("Origin: " + str(len(origin_addresses)))
            response = send_request(origin_addresses, dest_addresses)
            #Check if response is valid
            status = response["status"]
            if status != "OK":
                num_dests = len(dest_addresses)
                num_addresses = len(origin_addresses)
                raise ValueError(f"Error: Status is {status}, Destinations: {num_dests}, Origins: {num_addresses}")
            
            temp_matrix = np.array(build_matrix(response, type))
            if block.size == 0:
                block = temp_matrix
            else:
                block = np.hstack((block, temp_matrix))
        if r0 > 0:
            dest_addresses = addresses[q0 * num_addresses_per_request: q0 * num_addresses_per_request + r0]
            response = send_request(origin_addresses, dest_addresses)
            temp_matrix = np.array(build_matrix(response, type))
            if block.size == 0:
                block = temp_matrix
            else:
                block = np.hstack((block, temp_matrix))
        matrix += block.tolist()
    
    #Get the remaining r rows, if necessary
    if r > 0:
        origin_addresses = addresses[q*max_rows : q * max_rows + r]
        block = np.array([])
        for j in range(q0):
            dest_addresses = addresses[j * num_addresses_per_request: (j+1) * num_addresses_per_request]
            response = send_request(origin_addresses, dest_addresses)
            temp_matrix = np.array(build_matrix(response, type))
            if block.size == 0:
                block = temp_matrix
            else:
                block = np.hstack((block, temp_matrix))
        if r0 > 0:
            dest_addresses = addresses[q0 * num_addresses_per_request: q0 * num_addresses_per_request + r0]
            response = send_request(origin_addresses, dest_addresses)
            temp_matrix = np.array(build_matrix(response, type))
            if block.size == 0:
                block = temp_matrix
            else:
                block = np.hstack((block, temp_matrix))
        matrix+= block.tolist()
    return matrix
    

def get_coordinates(addresses):

    #Format the addresses correctly for the API call
    def encode_adresses(adresses):
        #Encodes adresses to valid URL
        adresses = [urllib.parse.quote(adress) for adress in adresses]
        return adresses
    
    addresses = encode_adresses(addresses)
    coordinates = [] #Array of tuples, (lng, lat)
    
    for address in addresses:
        #Construct request
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={config.API_KEY}"

        #Make request
        response = requests.get(url)

        #Process response
        if response.status_code == 200:
            api_status = response.json().get("status", "Status not available")
            print(f"Successfully called Geocoding API, Status {api_status}")
            location = response.json()["results"][0]["geometry"]["location"]
            coords = (location["lng"], location["lat"])
            coordinates.append(coords)
        else:
            print("Error calling Geocoding API: " + response.status_code)
    return coordinates

#Check whether pickup and dropoff times are possible, returns a 2d list [[trip_id, time it should take, travel time allowed]]
def check_validity(matrix, address_to_index, trips_dict):
    invalid_trips = []
    for id, trip in trips_dict.items():
        if trip["pick_up_time"] == 'WCall' or trip["los"] == 'S':
            continue
        pickup = standard_to_minutes(trip["pick_up_time"])
        dropoff = standard_to_minutes(trip["drop_off_time"])
        pickup_index = address_to_index[trip["pick_up_location"]]
        dropoff_index = address_to_index[trip["drop_off_location"]]
        travel_time = matrix[pickup_index][dropoff_index]
        time_difference = dropoff - pickup 
        if time_difference < travel_time:
            invalid_trips.append([id, travel_time, time_difference])
    return invalid_trips

def fix_invalid_trips(invalid_trips, data):
    for trip in invalid_trips:
        id = trip[0]
        t_needed = trip[1]
        t_given = trip[2]
        t_still_needed = t_needed - t_given #This number is > 0
        slack = 20
        #Minutes still needed to be allocated
        mins = t_still_needed - slack
        #Get the index of the corresponding time_window
        index = data["trips_dict"][id]["index"]
        if mins > 0:
            #Add remaining minutes needed if there are any to the pickup time
            data["time_windows"][index*2+2][1] = data["time_windows"][index*2+2][1] + mins

