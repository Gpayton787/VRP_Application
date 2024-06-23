import pandas as pd

#Model object
class Model:
    def __init__(self, matrix, num_vehicles, depot, capacity, pickups_deliveries):
        self.matrix = matrix
        self.num_vehicles = num_vehicles
        self.depot = depot
        self.capacity = capacity
        self.pickups_deliveries = pickups_deliveries
       

#Node object
class Node:
    def __init__(self, address, flag, time_window, patient_type, demand, trip_id):
        self.address = address
        self.flag = flag
        self.time_window = time_window
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
    #Create all our nodes
    #Also add directed edges between nodes to pickups_deliveries

    #Iterate row-wise through the dataframe
    for index in df.index:
        row = df.loc[index]

    


    

    
    

