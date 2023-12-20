from PyPDF2 import PdfReader
import re

def create_trip_dict(path):
    reader = PdfReader(path)
    page = reader.pages[0]
    text = page.extract_text()

    #Extract each trip

    trip_blocks = text.split('-' * 80) 
    #Remove first line
    trip_blocks = trip_blocks[1:]
    trips = []
    count = 0
    for block in trip_blocks:
        count += 1
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
    return trips

def main():
    path = "trips.pdf"
    create_trip_dict(path)

    
