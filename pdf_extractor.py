from PyPDF2 import PdfReader
import re
from utils.time import standard_to_minutes
import config

#Processes and returns the pdf file as a dictionary
def create_trip_dict(path):
    reader = PdfReader(path)
    raw_data = {}
    addresses = [] #List of addresses
    #Add depot to addresses
    addresses.append(config.DEPOT_ADDRESS)
    trips_dict = {} # Maps ID to trip info
    trips_list = [] #List of trips
    edges = [] #List the edges between pick up and drop off nodes
    edge_los = []
    time_windows = [] #Time windows for each node
    wcalls = []
    #Add depot to time windows
    time_windows.append([0, 100])
    address_to_index = {} #Maps the address to its index in the address list
    address_to_index[config.DEPOT_ADDRESS] = 0
    for page in reader.pages:
        #Extract text from page
        text = page.extract_text()
        trip_blocks = text.split('-' * 80) 
        #Remove first line
        line_w_date = trip_blocks[0]
        date = line_w_date.split('\n')[2]
        trip_blocks = trip_blocks[1:]
        for block in trip_blocks:
            lines = block.split('\n')
            #Get rid of empty elements
            trip_info = [line.strip() for line in lines if line.strip()]
            line1 = re.split(r' {3,}', trip_info[0])
            if line1[1] == '** CANCELED **':
                continue
            id = line1[0]
            line2 = re.split(r' {3,}', trip_info[1])
            name = line2[0]
            line3 = trip_info[2]
            m = re.match(r'[0-9][0-9]:[0-9][0-9]', line3)
            if m:
                pu_time = m.group(0)
            else:
                m = re.match(r'WCall', line3)
                if m:
                    pu_time = 'WCall'
                else:
                    print(line3)
                    raise Exception("No pickup time found")
            pu_loc = trip_info[3] + " " + trip_info[4]
            line6 = trip_info[5]
            m = re.match(r'[0-9][0-9]:[0-9][0-9]', line6 )
            if m:
                do_time = m.group(0)
            else:
                m = re.match(r'WCall', line3)
                if m:
                    pu_time = 'WCall'
                else:
                    print(line3)
                    raise Exception("No dropoff time found")
            do_loc = trip_info[6] + " " + trip_info[7]
            #Get LOS and Miles
            line9 = trip_info[8]
            los = ''
            miles = ''
            m = re.match(r'LOS: \w{0,3}', line9)
            if m:
                los = m.group(0).split(' ')[1]
            else:
                raise Exception("No LOS")
            m = re.search(r'Miles: (0|[1-9]\d*)(\.\d+)?', line9)
            if m:
                miles = m.group(0).split(' ')[1]
            else:
                raise Exception("No Miles")
            trip = {
                "name": name,
                "pick_up_time": pu_time,
                "pick_up_location": pu_loc,
                "drop_off_time": do_time,
                "drop_off_location": do_loc,
                "index": len(trips_list), #basically this index matches the trip to its corresponding edge
                "los": los,
                "miles": miles,
            }
            trips_dict[id] = trip
            #ONLY ADD WCALLS TO TRIP_DICT, this cannot mess up indexing
            if pu_time == 'WCall':
                wcalls.append(id)
                continue
            trips_list.append(id)
            #Populate address_to_index dict for adding edges
            if pu_loc not in address_to_index:
                address_to_index[pu_loc] = len(address_to_index)
            if do_loc not in address_to_index:
                address_to_index[do_loc] = len(address_to_index)
            edges.append([address_to_index[pu_loc], address_to_index[do_loc]])
            edge_los.append(los)
            #Create time windows for each location, there are two per edge
            #Convert standard time to minutes
            pu_time = standard_to_minutes(pu_time)
            do_time = standard_to_minutes(do_time)
            #Must arrive within 30 mins before pickup time
            time_windows.append([pu_time-10, pu_time+10])
            time_windows.append([pu_time-10, do_time+10])
    raw_data["trips_list"] = trips_list
    raw_data["trips_dict"] = trips_dict
    raw_data["addresses"] = list(address_to_index.keys())
    raw_data["edges"] = edges
    raw_data["edge_los"] = edge_los
    raw_data["time_windows"] = time_windows
    raw_data["address_to_index"] = address_to_index
    raw_data["wcalls"] = wcalls
    raw_data["file_name"] = path.split('.')[0]
    raw_data["date"] = date
    return raw_data

def main():
    path = "trips2.pdf"
    raw_data = create_trip_dict(path)
    print(raw_data["edge_los"])
    print(len(raw_data["edges"]))
    print(len(raw_data["edge_los"]))
    print(raw_data["date"])
    print(len(raw_data["trips_list"]))

    return 0
if __name__ == "__main__":
    main()


