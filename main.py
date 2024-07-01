#Imports
import sys
import pandas as pd
from pdf_extractor import create_trip_dict
from solver import create_data_model, solver
from utils.helper import check_validity, fix_invalid_trips
from pdf_creation.pdf_creator import create_pdf
from parsing import parser

#Define global variables 
service_area = []
num_vehicles = 0
capacity = 0
wheelchair = False
expected_columns = ["trip_id", "name", "pickup_time", "pickup_address", "dropoff_time", "dropoff_address", "los", "miles", "num_vehicles", "capacity", "service_area", "date", "depot"]


def main():
    ##PARSING MODULE
    #Take command line input
    n = len(sys.argv)
    if (n != 2):
        print("Usage: python3 main.py <csv_file>")
        return
    file_path = sys.argv[1]
    if file_path[-4:] != ".csv":
        print("Please provide a csv file")
        return
    
    #Extract data from CSV into a dataframe
    df = pd.read_csv(file_path)

    #Validate the columns
    df.columns.to_list()
    for col in expected_columns:
        if col not in df.columns.to_list():
            print(f"Column {col} is missing")
            return
        
    print(df)
    #Process the data for modeling
    # proccess_data(df)


    return

    #Create the data model for the solver
    data = create_data_model()

    #Process the data
    invalid_trips = check_validity(data["matrix"], data["address_to_index"], data["trips_dict"])
    #Fix invalid trips for the solver
    fix_invalid_trips(invalid_trips)
    print(invalid_trips)
    #Call the solver
    response = solver(data)

    #Generate the pdf

if __name__ == "__main__":
    main()




