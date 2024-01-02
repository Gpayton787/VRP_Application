from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys
from utils.helper import create_node_mapping

def create_data_model():
    """Stores the data for the problem."""
    data = {}

    data["distance_matrix"] = [
        # fmt: off
        [0, 20821, 50395, 1405, 56749, 17835, 2090, 54103, 52599, 45675], 
        [20826, 0, 35456, 19112, 55104, 3148, 18793, 39164, 37660, 30736], 
        [50085, 34772, 0, 46804, 76486, 35831, 47684, 6098, 15785, 5532], 
        [1126, 19524, 46974, 0, 57291, 17010, 1515, 50683, 49178, 42255], 
        [57198, 55158, 77143, 57740, 0, 57448, 57413, 80851, 79281, 72423], 
        [17837, 3038, 35842, 16223, 57393, 0, 15802, 39550, 38046, 31122], 
        [2292, 18786, 45909, 1523, 56954, 15800, 0, 49617, 48113, 41189], 
        [53909, 38596, 6394, 50628, 80310, 39655, 51508, 0, 21723, 12052], 
        [54037, 38725, 15789, 50756, 80420, 39784, 51637, 21758, 0, 13400], 
        [45389, 30077, 5532, 42108, 71791, 31136, 42989, 11661, 13477, 0],
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
    data["num_vehicles"] = 4
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")


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


    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        #Convert from NodeIndex to actual distance matrix index
        if from_node in data["node_to_index"]:
            from_node = data["node_to_index"][from_node]
        if to_node in data["node_to_index"]:
            to_node = data["node_to_index"][to_node]
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

    # Define Transportation Requests.
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

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        print(routing.status())
    else:
        print('no solution')
        print(routing.status())


if __name__ == "__main__":
    main()