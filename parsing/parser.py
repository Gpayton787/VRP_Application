import pandas as pd
import myconstants
from ..utils.helper import create_matrix

#Model object
class Model:
    def __init__(self, addresses, num_vehicles, depot, capacity, pickups_deliveries, address_to_matrix_index):
        self.matrix = create_matrix(addresses)
        self.num_vehicles = num_vehicles
        self.depot = depot
        self.capacity = capacity
        self.pickups_deliveries = pickups_deliveries
        self.address_to_matrix_index = address_to_matrix_index

#Node object
class Node:
    def __init__(self, address, flag, time, patient_type, demand, trip_id):
        self.address = address
        self.flag = flag #pickup or delivery
        self.time = time
        self.patient_type = patient_type
        self.demand = demand
        self.trip_id = trip_id

    def __str__(self):
        return f"Address: {self.address}, Flag: {self.flag}, Time Window: {self.time_window}, Patient Type: {self.patient_type}, Demand: {self.demand}, Trip ID: {self.trip_id}"

#Functions:
#1. Reads the CSV file into a pandas DataFrame
#2. Processes the data to be used in the solver (See README for processing information)
def csv_reader(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Return the DataFrame
    return df

def create_objects(df):
    #List of nodes (each node represents a single stop)
    nodes = []
    #Maps the address to it's distance matrix index
    address_to_matrix_index = {}
    #List of edges {x,y} where x and y are indexes of nodes
    edges = []

    #Iterate row-wise through the dataframe to create nodes 
    for index in df.index:
        row = df.loc[index]
        #Add a seperate node for pickup and dropoff
        node = Node(address=row["pickup_address"], flag=myconstants.PICKUP, time=row["pickup_time"], patient_type=row["los"], demand=1, trip_id=row["trip_id"])
        nodes.append(node)
        node = Node(address=row["dropoff_address"], flag=myconstants.DROPOFF, time=row["dropoff_time"], patient_type=row["los"], demand=-1, trip_id=row["trip_id"])
        nodes.append(node)
        #Add mappings
        if row["pickup_address"] not in address_to_matrix_index:
            address_to_matrix_index[row["pickup_address"]] = len(address_to_matrix_index)
        if row["dropoff_address"] not in address_to_matrix_index:
            address_to_matrix_index[row["dropoff_address"]] = len(address_to_matrix_index)
        #Add edge
        edges.append((address_to_matrix_index[row["pickup_address"]], address_to_matrix_index[row["dropoff_address"]]))

    #Unique set of addresses for the model
    addresses = list(address_to_matrix_index.keys())


        


    



    


    

    
    

