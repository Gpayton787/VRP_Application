import math
from matplotlib import pyplot as plt

def output_data(data):
  """Prints data to console."""
  print(f"Addreses ({len(data['addresses'])}): {data['addresses']}")
  print(f"Number of Nodes: {data['num_nodes']}")
  print()
  print(f"Time Windows ({len(data['time_windows'])}): {data['time_windows']}")


def plot_location(location, axes, color, location_number):
  axes.scatter(
      location[0],
      location[1],
      s=1000,
      facecolors='white',
      edgecolors=color,
      linewidths=2)
  
def plot_solution(locations, manager, routing, solution, loc, marker_size):
  height = 8
  fig, axes = plt.subplots(figsize=(1.7 * height, height))
  axes.grid(True)
  axes.set_xticks(list(set([x for (x, y) in locations])))
  axes.set_xticklabels([])
  axes.set_yticks(list(set([y for (x, y) in locations])))
  axes.set_yticklabels([])
  axes.set_axisbelow(True)
  max_route_distance = 0
  google_colors = [
      r'#4285F4', r'#EA4335', r'#FBBC05', r'#34A853', r'#101010', r'#FFFFFF'
  ]
  for vehicle_id in range(manager.GetNumberOfVehicles()):
    previous_index = routing.Start(vehicle_id)
    while not routing.IsEnd(previous_index):
      index = solution.Value(routing.NextVar(previous_index))
      start_node = manager.IndexToNode(previous_index)
      end_node = manager.IndexToNode(index)
      start = locations[start_node]
      end = locations[end_node]
      delta_x = end[0] - start[0]
      delta_y = end[1] - start[1]
      delta_length = math.sqrt(delta_x**2 + delta_y**2)
      unit_delta_x = delta_x / delta_length
      unit_delta_y = delta_y / delta_length
      axes.arrow(
          start[0] + (marker_size / 2) * unit_delta_x,
          start[1] + (marker_size / 2) * unit_delta_y,
          (delta_length - marker_size) * unit_delta_x,
          (delta_length - marker_size) * unit_delta_y,
          head_width=20,
          head_length=20,
          facecolor=google_colors[vehicle_id],
          edgecolor=google_colors[vehicle_id],
          length_includes_head=True,
          width=5)
      previous_index = index
      node_color = 'black' if routing.IsEnd(
          previous_index) else google_colors[vehicle_id]
      plot_location(end, axes, node_color, end_node)