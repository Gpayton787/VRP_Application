from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import sys 
import math

from utils.helper import create_node_mapping
from utils.time import minutes_to_standard

height = 8

def index_to_location(index, data):
    if index in data["node_to_index"]:
        index = data["node_to_index"][index]
    return index

def index_to_location_name(index, data):
    return data["addresses"][index_to_location(index, data)]
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
        r'#4285F4', r'#EA4335', r'#FBBC05', r'#34A853', r'#101010', r'#FFFFFF'
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
    plt.show()



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
    #Convert to minutes
    n = len(data["matrix"])
    for i in range(n):
        for j in range(n):
            data["matrix"][i][j] = math.ceil(data["matrix"][i][j] / 60)
    edges = [
        [1, 2], [3, 4], [4, 3], [2, 1], [5, 4], [4, 5], [6, 2], [2, 6], [7, 8], [9, 2], [8, 7], [2, 9]
    ]
    node_data = create_node_mapping(edges)
    data["pickups_deliveries"] = node_data["new_edges"]
    data["node_to_index"] = node_data["node_to_index"]
    data["node_to_trip"] = node_data["node_to_trip"]
    data["num_nodes"] = node_data["num_nodes"]
    data["demands"] = node_data["node_to_demand"]
    data["vehicle_capacities"] = 3
    data["time_windows"] = [
        [0, 100], [310, 370], [350, 410], 
        [345, 405], [345, 405], [375, 435], 
        [423, 483], [390, 450], [424, 484], 
        [420, 480], [472, 532], [525, 585], 
        [575, 635], [765, 825], [771, 831], 
        [780, 840], [845, 905], [350, 410], 
        [382, 442], [360, 420], [382, 442], 
        [395, 455], [426, 486], [435, 495], 
        [454, 514]
    ]
    data["num_vehicles"] = 4
    data["depot"] = 0
    data["locations"] = [(-119.7955506, 36.3080387), (-119.6327801, 36.3612236), (-119.2913175, 36.3157652), (-119.7862348, 36.30631839999999), (-119.7631925, 36.7798332), (-119.6485127, 36.3470397), (-119.7838819, 36.3164792), (-119.2562081, 36.34114), (-119.3378978, 36.2199703), (-119.3458828, 36.3173923)]
    data["addresses"] = ['1005 Columbus Way Lemoore, CA 93245', '889 Meadow View Rd Hanford, CA 93230-2358', '1646 S Court St Visalia, CA 93277-4962', '335 W Cinnamon Dr, Apt. APT 162 Lemoore, CA 93245-9413', '3707 E Shields Ave Fresno, CA 93726-7029', '202 W Terrace Dr, Bldg. House Hanford, CA 93230-2073', '203 W Hazelwood Dr, Bldg. 5596704299 Lemoore, CA 93245-1931', '3307 E Houston Ave Visalia, CA 93292-4013', '793 N Cherry St Tulare, CA 93274-2205', '4929 W Howard Ave, Bldg. House Visalia, CA 93277-3416']
    data["trips_list"] = ['01-1766-A', '01-631-A', '01-631-B', '01-1766-B', '01-492-A', '01-492-B', '01-114-A', '01-114-B', '01-2160-A', '01-2365-A', '01-2160-B', '01-2365-B']
    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
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
    if solution:
        print_solution(data, manager, routing, solution)
        print(routing.status())
    else:
        print('no solution')
        print(routing.status())

    plot_solution(data["locations"], solution, manager, routing, data)


if __name__ == "__main__":
    main()