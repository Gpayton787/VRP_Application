from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys
from pdf_extractor import create_trip_dict
from utils.helper import create_matrix, create_node_mapping, get_coordinates
from utils.time import minutes_to_standard
import pickle
import os

#Define instance variables
file_path = "trips.pdf"
type_of_matrix = "time"
height = 7

def does_file_exist(path):
    return os.path.exists(path)
 

def index_to_trip_id(index, data):
    if index == 0:
        return "Depot"
    return data["trips_list"][data["node_to_trip"][index]]

def plot_solution(locations, solution, manager, routing, data):
    import matplotlib.pyplot as plt
    import numpy as np
    # Plotting
    locations = np.array(locations)
    fig, ax = plt.subplots(figsize=(1.7*height,height))
    # Plot all the nodes as black dots.
    ax.plot(locations[:, 0], locations[:, 1], 'k.', markersize=10)
    # Plot the depot as a red diamond.
    ax.plot(locations[0, 0], locations[0, 1], 'rD', markersize=12)
    # Plot the solution.
    google_colors = [
        r'#4285F4', r'#950952', r'#F3C98B', r'#99D19C', r'#FFB8DE', r'#009FB7', r'#668586', r'#A7ACD9'
    ]
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            new_index = manager.IndexToNode(index)
            if new_index in data["node_to_index"]:
                new_index = data["node_to_index"][new_index]
            route.append(new_index)
        # Convert route to numpy array for plotting
        route = np.array(route)
        # Plot the route
        ax.plot(locations[route, 0], locations[route, 1], google_colors[vehicle_id], linewidth=3)
        break
    plt.show()

def create_response_object(data, manager, routing, solution):
    #Get a list of dropped trips
    dropped_trips = []
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if solution.Value(routing.NextVar(node)) == node:
            trip = index_to_trip_id(manager.IndexToNode(node), data)
            if trip not in dropped_trips:
                dropped_trips.append(trip)
    #Get trip assignments
    def get_routes(data, solution, routing, manager):
        # Get vehicle routes and store them in a two dimensional array whose
        # i,j entry is the jth location visited by vehicle i along its route.
        routes = []
        for route_nbr in range(routing.vehicles()):
            index = routing.Start(route_nbr)
            route = [index_to_trip_id(manager.IndexToNode(index), data)]
            while not routing.IsEnd(index):
                index = solution.Value(routing.NextVar(index))
                trip = index_to_trip_id(manager.IndexToNode(index), data)
                if trip not in route:
                    route.append(trip)
            routes.append(route)
        return routes
    
    routes = get_routes(data, solution, routing, manager)

    #Get route instructions
    time_dimension = routing.GetDimensionOrDie("Time")
    instructions = []
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route_load = 0
        route_instructions = []
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            route_load += data["demands"][manager.IndexToNode(index)]
            trip_id = index_to_trip_id(manager.IndexToNode(index), data)
            time_window = [minutes_to_standard(solution.Min(time_var)), minutes_to_standard(solution.Max(time_var))]
            load = route_load
            route_instructions.append({"trip_id": trip_id, "time_window": time_window, "load": load})
            #move to next node
            index = solution.Value(routing.NextVar(index))
        instructions.append(route_instructions)
    response = {}
    response["dropped_trips"] = dropped_trips
    response["routes"] = routes
    response["instructions"] = instructions

    return response


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    # Display dropped nodes.
    dropped_nodes = "Dropped nodes:"
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if solution.Value(routing.NextVar(node)) == node:
            dropped_nodes += f" {manager.IndexToNode(node)}"
    #Display routes
    print(dropped_nodes)
    time_dimension = routing.GetDimensionOrDie("Time")
    total_time = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_load = 0
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            route_load += data["demands"][manager.IndexToNode(index)]
            plan_output += (
                f"{index_to_trip_id(manager.IndexToNode(index), data)}"
                f" Time({minutes_to_standard(solution.Min(time_var))},{minutes_to_standard(solution.Max(time_var))})"
                f" Load({route_load})"
                " -> "
            )
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += (
            f"{index_to_trip_id(manager.IndexToNode(index), data)}"
            f" Time({minutes_to_standard(solution.Min(time_var))},{minutes_to_standard(solution.Max(time_var))})\n"
        )
        plan_output += f"Time of the route: {solution.Min(time_var)}min\n"
        print(plan_output)
        total_time += solution.Min(time_var)
    print(f"Total time of all routes: {total_time}min")

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
    #Check if matrix and locations have already been created
    file_name = raw_data["file_name"]
    matrix_path = './cache/' + file_name + '_matrix.pkl'
    if does_file_exist(matrix_path):
        with open(matrix_path, 'rb') as file:
            data["matrix"] = pickle.load(file)
    else:
        data["matrix"] = create_matrix(raw_data["addresses"], type_of_matrix)
        #pickle it
        with open(matrix_path, 'wb') as file:
            pickle.dump(data["matrix"], file)
    locations_path = './cache/' + file_name + '_locations.pkl'
    if does_file_exist(locations_path):
        with open(locations_path, 'rb') as file:
            data["locations"] = pickle.load(file)
    else:
        data["locations"] = get_coordinates(data["addresses"])
        #pickle it
        with open(locations_path, 'wb') as file:
            pickle.dump(data["locations"], file)
    return data

def solver(data):

    #Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(
        data["num_nodes"], data["num_vehicles"], data["depot"]
    )
    #Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        if from_node in data["node_to_index"]:
            from_node = data["node_to_index"][from_node]
        if to_node in data["node_to_index"]:
            to_node = data["node_to_index"][to_node]
        return data["matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

     # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimension(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Add Time Windows constraint.
    time = "Time"
    routing.AddDimension(
        transit_callback_index,
        sys.maxsize,  # allow waiting time
        sys.maxsize,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data["time_windows"]):
        if location_idx == data["depot"]:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data["depot"]
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data["time_windows"][depot_idx][0], data["time_windows"][depot_idx][1]
        )
    # Instantiate route start and end times to produce feasible times.
    for i in range(data["num_vehicles"]):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    #Define Transportation requests
    for request in data["pickups_deliveries"]:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
        )
        routing.solver().Add(
            time_dimension.CumulVar(pickup_index)
            <= time_dimension.CumulVar(delivery_index)
        )
    # Allow to drop nodes.
    penalty = 1000
    for node in range(1, data["num_nodes"]):
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)


     # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.

    #Prepare return data and return it in a dictionary
    # return create_response_object(data, manager, routing, solution)

    if solution:
        print_solution(data, manager, routing, solution)
        print(routing.status())
        # plot_solution(data["locations"], solution, manager, routing, data)
    else:
        print('no solution')
        print(routing.status())
    return create_response_object(data, manager, routing, solution)
    

def main():
    arr = [0,5,3]
    file_name = 'binga'
    locations_path = './cache/' + file_name + '_locations.pkl'

    with open(locations_path, 'wb') as file:
        pickle.dump(arr, file)


if __name__ == "__main__":
    main()