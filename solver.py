import urllib.parse
from pdf_extracter import create_trip_dict
import requests
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys
import config

file_path = "trips.pdf"


def encode_adresses(adresses):
    #Encodes adresses to valid URL
    adresses = [urllib.parse.quote(adress) for adress in adresses]
    return adresses

def create_node_mapping(edges):
    extra_nodes = 0
    #map duplicate nodes to their actual location
    node_to_index = {}
    new_edges = []
    seen = set()
    for i, edge in enumerate(edges):
        #check for and process duplicate nodes
        new_edge = []
        if edge[0] not in seen:
            seen.add(edge[0])
            new_edge.append(edge[0])
        else:
            extra_nodes += 1
            node_to_index[len(seen)+extra_nodes] = edge[0]
            new_edge.append(len(seen)+extra_nodes)
            #extra_nodes + len(seen) is the index of the duplicate node which corresponds to the actual node
        if edge[1] not in seen:
            seen.add(edge[1])
            new_edge.append(edge[1])
        else:
            extra_nodes += 1
            node_to_index[len(seen)+extra_nodes] = edge[1]
            new_edge.append(len(seen)+extra_nodes)
        new_edges.append(new_edge)
    return new_edges, node_to_index

def create_distance_matrix(addresses):

    encoded = encode_adresses(addresses)

    test_addresses = ["16920 Glen Oak Run, Derwood, MD", "19225 Montgomery Village Ave, Montgomery Village, MD", "8201 Emory Grove Rd, Gaithersburg, MD"]

    #Construct request URL
    origins = '|'.join(encoded)
    test_origins = '|'.join(test_addresses)

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={origins}&origins={origins}&units=imperial&key={config.API_KEY}"

    #Send request
    response = requests.get(url)

    matrix = []

    #Process response
    if response.status_code == 200:
        print(response.status_code)

        for row in response.json()["rows"]:
            matrix_row = []
            for element in row["elements"]:
                matrix_row.append(element["distance"]["value"])
            matrix.append(matrix_row)
    else:
        print("Error: ", response.status_code)
    return matrix

def create_data_model():
    #Stores problem data
    raw_data = create_trip_dict(file_path)
    data = {}
    data["distance_matrix"] = create_distance_matrix(raw_data["addresses"])
    data["num_vehicles"] = 1
    data["depot"] = 0
    edges, node_map = create_node_mapping(raw_data["edges"])
    data["pickups_deliveries"] = edges
    data["node_map"] = node_map
    return data


def print_solution(data, manager, routing, solution):
    #Prints solution on console
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        print(plan_output)
        total_distance += route_distance
    print(f"Total Distance of all routes: {total_distance}m")

def main():

    #Instantiate the data 
    data = create_data_model()
    print(data["edges"])
    print(data["node_map"])

    return 

    #Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )
    #Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

     # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        sys.maxsize,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    for request in data["pickups_deliveries"]:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
        )
        routing.solver().Add(
            distance_dimension.CumulVar(pickup_index)
            <= distance_dimension.CumulVar(delivery_index)
        )


     # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    print(solution)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    print(data)
    
    


if __name__ == "__main__":
    main()