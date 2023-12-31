from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys
from pdf_extractor import create_trip_dict
from utils.helper import create_matrix, create_node_mapping, get_coordinates
import pickle

#Define instance variables
file_path = "trips.pdf"
type_of_matrix = "time"

def create_data_model(raw_data, num_vehicles, capacity):
    #Stores problem data
    data = {}
    data["addresses"] = raw_data["addresses"]
    data["address_to_index"] = raw_data["address_to_index"]
    data["trips_list"] = raw_data["trips_list"]
    data["trips_dict"] = raw_data["trips_dict"]
    data["num_vehicles"] = num_vehicles
    data["depot"] = 0
    node_data = create_node_mapping(raw_data["edges"])
    data["pickups_deliveries"] = node_data["new_edges"]
    data["num_nodes"] = node_data["num_nodes"]
    data["node_to_index"] = node_data["node_to_index"]
    data["node_to_trip"] = node_data["node_to_trip"]
    data["demands"] = node_data["node_to_demand"]
    data["vehicle_capacities"] = capacity
    data["time_windows"] = raw_data["time_windows"]
    # data["matrix"] = create_matrix(raw_data["addresses"], type_of_matrix)
    # data["locations"] = get_coordinates(data["addresses"])
    # Load the matrix from the binary file
    with open('./test_data/matrix.pkl', 'rb') as file:
        loaded_matrix = pickle.load(file)
    with open('./test_data/locations.pkl', 'rb') as file:
        loaded_locations = pickle.load(file)
    data["matrix"] =loaded_matrix
    data["locations"] = loaded_locations
    return data

def main():

    #Instantiate the data 
    data = create_data_model()

    print(data["matrix"])
    return

    #Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(data["num_nodes"]), data["num_vehicles"], data["depot"]
    )
    #Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["matrix"][from_node][to_node]
    
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