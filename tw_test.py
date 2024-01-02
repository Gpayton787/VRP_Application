from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys

from utils.helper import create_node_mapping
from utils.time import seconds_to_standard, standard_to_seconds

def create_data_model():
    """Stores the data for the problem."""
    data = {}

    data["matrix"] = [
        # fmt: off
        [0, 1256, 2012, 165, 2364, 1132, 270, 2141, 2087, 1890],
        [1278, 0, 1474, 1129, 2340, 317, 1139, 1603, 1549, 1352],
        [2014, 1484, 0, 1880, 2827, 1573, 1937, 422, 1103, 571], 
        [133, 1160, 1881, 0, 2359, 1043, 159, 2011, 1956, 1760], 
        [2383, 2359, 2873, 2393, 0, 2517, 2384, 3002, 2936, 2751], 
        [1109, 294, 1569, 1000, 2503, 0, 986, 1699, 1644, 1448], 
        [234, 1134, 1941, 165, 2336, 1010, 0, 2071, 2016, 1820], 
        [2117, 1587, 558, 1983, 2929, 1675, 2039, 0, 1362, 726], 
        [2164, 1634, 1107, 2030, 2968, 1722, 2087, 1378, 0, 942], 
        [1895, 1364, 569, 1760, 2707, 1453, 1817, 683, 874, 0]
        # fmt: on
    ]
    edges = [
        [1, 2], [3, 4], [4, 3], [2, 1], [5, 4], [4, 5], [6, 2], [2, 6], [7, 8], [9, 2], [8, 7], [2, 9]
    ]

    node_data = create_node_mapping(edges)
    data["pickups_deliveries"] = node_data["new_edges"]
    data["node_to_index"] = node_data["node_to_index"]
    data["num_nodes"] = node_data["num_nodes"]
    data["demands"] = node_data["node_to_demand"]
    data["vehicle_capacities"] = 3
    data["time_windows"] = [
        [0, 6000], 
        [18600, 20400], [21000, 22800], [20700, 22500], [20700, 22500], [22500, 24300], 
        [25380, 27180], [23400, 25200], [25440, 27240], [25200, 27000], [28320, 30120], 
        [31500, 33300], [34500, 36300], [45900, 47700], [46260, 48060], [46800, 48600], 
        [50700, 52500], [21000, 22800], [22920, 24720], [21600, 23400], [22920, 24720], 
        [23700, 25500], [25560, 27360], [26100, 27900], [27240, 29040]
        ]
    data["num_vehicles"] = 8
    data["depot"] = 0
    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    time_dimension = routing.GetDimensionOrDie("Time")
    total_time = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += (
                f"{manager.IndexToNode(index)}"
                f" Time({solution.Min(time_var)},{solution.Max(time_var)})"
                " -> "
            )
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += (
            f"{manager.IndexToNode(index)}"
            f" Time({solution.Min(time_var)},{solution.Max(time_var)})\n"
        )
        plan_output += f"Time of the route: {solution.Min(time_var)}min\n"
        print(plan_output)
        total_time += solution.Min(time_var)
    print(f"Total time of all routes: {total_time}min")

def main():
    """Entry point of the program."""
    # Instantiate the data problem.

    data = create_data_model()
  
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        data["num_nodes"], data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
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


    # Define Transportation Requests.
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

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        print(routing.status())
    else:
        print('no solution')
        print(routing.status())


if __name__ == "__main__":
    main()