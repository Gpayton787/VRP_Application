from PyPDF2 import PdfReader
import re

def create_trip_dict(path):
    reader = PdfReader(path)
    raw_data = {}
    addresses = []
    #Add depot to addresses
    addresses.append("1005 Columbus Way Lemoore, CA 93245")
    trips = []
    edges = []
    address_to_index = {}
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
            id = trip_info[0].split(' ')[0]
            pattern = r"^[A-Z]+,\s[A-z]+\s[A-Z]?"
            match = re.search(pattern, trip_info[1])
            name = ""
            if match:
                name = match.group(0)
            else:
                name = "Not Found, check ur code"
            pick_up_time= trip_info[2].split(' ')[0]
            pick_up_location = trip_info[3].strip() + " " + trip_info[4].strip()
            drop_off_time = trip_info[5].split(' ')[0]
            drop_off_location = trip_info[6].strip() + " " + trip_info[7].strip()
            trip = {
                "id": id,
                "name": name,
                "pick_up_time": pick_up_time,
                "pick_up_location": pick_up_location,
                "drop_off_time": drop_off_time,
                "drop_off_location": drop_off_location
            }
            trips.append(trip)
            if pick_up_location not in addresses:
                addresses.append(pick_up_location)
            if drop_off_location not in addresses:
                addresses.append(drop_off_location)
            #Populate address_to_index dict for adding edges
            if pick_up_location not in address_to_index:
                address_to_index[pick_up_location] = len(address_to_index)
            if drop_off_location not in address_to_index:
                address_to_index[drop_off_location] = len(address_to_index)
            edges.append([address_to_index[pick_up_location], address_to_index[drop_off_location]])
    raw_data["trips"] = trips
    raw_data["addresses"] = addresses
    raw_data["edges"] = edges
    return raw_data

def main():
    path = "trips.pdf"
    data = create_trip_dict(path)
    print(data)

    
if __name__ == "__main__":
    main()