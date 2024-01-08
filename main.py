#Imports
from pdf_extractor import create_trip_dict
from solver import create_data_model
from utils.helper import check_validity, create_matrix
import numpy as np
#Main entry point for the application



def main():
    #Get user input

    #Parameters
    file_path = "trips1.pdf"
    num_vehicles = 4
    capacity = 3



    #Create the data model
    raw_data = create_trip_dict(file_path)
    data = create_data_model(raw_data, num_vehicles, capacity)
    invalid_trips = check_validity(data["matrix"], data["address_to_index"], data["trips_dict"])
    print(invalid_trips)

    
    return 
   

if __name__ == "__main__":
    main()




