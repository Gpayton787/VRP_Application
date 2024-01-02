import requests
import config
import urllib.parse

#Helper functions for formatting data to use with OR-Tools

#Returns necessary node information to model the problem
def create_node_mapping(edges):
    node_data = {}
    #map duplicate nodes to their actual location
    node_to_index = {}
    #Record whether a node is a pick-up or drop-off
    node_to_demand = {} #Can be either 1 or -1
    #Depot has demand 0
    node_to_demand[0] = 0
    #Store new unique edge list
    new_edges = []
    #Keep track of indexes
    seen = set()
    for edge in edges:
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
        node_to_demand[new_edge[-1]] = 1
        if edge[1] not in seen:
            seen.add(edge[1])
            new_edge.append(edge[1])
        else:
            index = len(seen)+1
            seen.add(index)
            node_to_index[index] = edge[1]
            new_edge.append(index)
        node_to_demand[new_edge[-1]] = -1
        new_edges.append(new_edge)
    node_data["new_edges"] = new_edges
    node_data["node_to_index"] = node_to_index
    #Add one to account for 0 index (depot)
    node_data["num_nodes"] = len(seen)+1
    node_data["node_to_demand"] = node_to_demand
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
            row_list = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
            matrix.append(row_list)
    return matrix


#Arguments: A list of addresses, the type of matrix (either distance or time)
def create_matrix(addresses, type):
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses)
    max_rows = max_elements // num_addresses
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    matrix = []

    #Send q requests, returning max rows per request
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i+1) * max_rows]
        response = send_request(origin_addresses, dest_addresses)
        matrix += build_matrix(response, type)
    
    #Get the remaining r rows, if necessary
    if r > 0:
        origin_addresses = addresses[q*max_rows : q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses)
        matrix+= build_matrix(response)
    return matrix
    

def get_coordinates(addresses):

    #Format the addresses correctly for the API call
    def encode_adresses(adresses):
        #Encodes adresses to valid URL
        adresses = [urllib.parse.quote(adress) for adress in adresses]
        return adresses
    
    addresses = encode_adresses(addresses)
    coordinates = [] #Array of tuples
    
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





