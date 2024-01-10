#Imports
from pdf_extractor import create_trip_dict
from solver import create_data_model, solver
from utils.helper import check_validity, create_matrix
import numpy as np
#Main entry point for the application



def main():
    #Get user input

    #Parameters
    file_path = "trips2.pdf"
    num_vehicles = 4
    capacity = 3



    #Create the data model
    raw_data = create_trip_dict(file_path)
    data = create_data_model(raw_data, num_vehicles, capacity)
    invalid_trips = check_validity(data["matrix"], data["address_to_index"], data["trips_dict"])
    print(invalid_trips)
    #Fix invalid trips for the solver
    for trip in invalid_trips:
        id = trip[0]
        t_needed = trip[1]
        t_given = trip[2]
        t_still_needed = t_needed - t_given #This number is > 0
        slack = 20
        #Minutes still needed to be allocated
        mins = t_still_needed - slack
        #Get the index of the corresponding time_window
        index = data["trips_dict"][id]["index"]
        if mins > 0:
            #Add remaining minutes needed if there are any to the pickup time
            data["time_windows"][index*2+2][1] = data["time_windows"][index*2+2][1] + mins
        print(data["time_windows"][index*2+2][1] - data["time_windows"][index*2+1][0])
    
    solver(data)

    return 
   

if __name__ == "__main__":
    main()




