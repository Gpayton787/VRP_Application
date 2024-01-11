#Imports
from pdf_extractor import create_trip_dict
from solver import create_data_model, solver
from utils.helper import check_validity
from utils.pdf import create_pdf


#Main entry point for the application
def main():
    #Get user input

    #Parameters
    file_path = "trips3.pdf"
    num_vehicles = 4
    capacity = 3
    wheelchair = False
    service_area = []

    #Extract data from pdf
    raw_data = create_trip_dict(file_path)
    #Create the data model for the solver
    data = create_data_model(raw_data, num_vehicles, capacity)

    #Process the data
    invalid_trips = check_validity(data["matrix"], data["address_to_index"], data["trips_dict"])
    print("Invalid Trips: ", invalid_trips)
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
    
    #Call the solver
    response = solver(data)
    
    #Print out the response data:
    tot = len(data["trips_list"])
    print("Total Trips: ", tot )
    print(f"Dropped Trips ({len(response['dropped_trips'])}): {response['dropped_trips']}")
    print("Trip assignments: ")
    for i, route in enumerate(response["routes"]):
        print(f"Route {i} Amount: {len(route)}")
        print(route)
    print("Trip sequences: ")
    for i, instructions in enumerate(response["instructions"]):
        print(f"Route {i} Instructions: ")
        print(instructions) 
        print("---"*10)

    





    

    return 
   

if __name__ == "__main__":
    main()




