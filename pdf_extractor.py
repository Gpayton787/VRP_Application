from PyPDF2 import PdfReader
import re
from utils.time import standard_to_minutes

#Processes and returns the pdf file as a dictionary
def create_trip_dict(path):
    reader = PdfReader(path)
    raw_data = {}
    addresses = [] #List of addresses
    #Add depot to addresses
    addresses.append("1005 Columbus Way Lemoore, CA 93245")
    trips_dict = {} # Maps ID to trip info
    trips_list = [] #List of trips
    edges = [] #List the edges between pick up and drop off nodes
    time_windows = [] #Time windows for each node
    wcalls = []
    #Add depot to time windows
    time_windows.append([0, 100])
    address_to_index = {} #Maps the address to its index in the address list
    address_to_index["1005 Columbus Way Lemoore, CA 93245"] = 0
    for page in reader.pages:
        #Extract text from page
        text = page.extract_text()
        trip_blocks = text.split('-' * 80) 
        #Remove first line
        trip_blocks = trip_blocks[1:]
        for block in trip_blocks:
            lines = block.split('\n')
            trip_info = [line.strip() for line in lines if line.strip()]
            if '** CANCELED **' in trip_info[0]:
                continue
            id = trip_info[0].split(' ')[0]
            pattern = r"^([A-Z]+[\s-])*([A-Z]+,)*\s([A-Z])+([\s-][A-Z]+)*"
            match = re.search(pattern, trip_info[1])
            name = ""
            if match:
                name = match.group(0)
            else:
                raise ValueError(f"Error: Cannot find name for trip {id}")
            pick_up_time= trip_info[2].split(' ')[0]
            pick_up_location = trip_info[3].strip() + " " + trip_info[4].strip()
            drop_off_time = trip_info[5].split(' ')[0]
            drop_off_location = trip_info[6].strip() + " " + trip_info[7].strip()
            trip = {
                "name": name,
                "pick_up_time": pick_up_time,
                "pick_up_location": pick_up_location,
                "drop_off_time": drop_off_time,
                "drop_off_location": drop_off_location,
                "index": len(trips_list) #basically this index matches the trip to its corresponding edge
            }
            trips_dict[id] = trip
            #ONLY ADD WCALLS TO TRIP_DICT, this cannot mess up indexing
            if pick_up_time == 'WCall':
                wcalls.append(id)
                continue
            trips_list.append(id)
            #Populate address_to_index dict for adding edges
            if pick_up_location not in address_to_index:
                address_to_index[pick_up_location] = len(address_to_index)
            if drop_off_location not in address_to_index:
                address_to_index[drop_off_location] = len(address_to_index)
            edges.append([address_to_index[pick_up_location], address_to_index[drop_off_location]])
            #Create time windows for each location, there are two per edge
            #Convert standard time to minutes
            pick_up_time = standard_to_minutes(pick_up_time)
            drop_off_time = standard_to_minutes(drop_off_time)
            #Must arrive within 30 mins before pickup time
            time_windows.append([pick_up_time-10, pick_up_time+10])
            time_windows.append([drop_off_time-10, drop_off_time+10])

    raw_data["trips_list"] = trips_list
    raw_data["trips_dict"] = trips_dict
    raw_data["addresses"] = list(address_to_index.keys())
    raw_data["edges"] = edges
    raw_data["time_windows"] = time_windows
    raw_data["address_to_index"] = address_to_index
    raw_data["wcalls"] = wcalls
    return raw_data

def main():
    path = "trips2.pdf"
    data = create_trip_dict(path)
if __name__ == "__main__":
    main()

#TEXT MUST FOLLOW THE FORMAT OF THE EXAMPLE PDF
def process_text(text):
    for line in text:
        if '** NEW **' in line:
            pass

