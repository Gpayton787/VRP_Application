from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
import pickle

def create_pdf(output_file, response):
    # Create a PDF document
    pdf = Canvas(output_file, pagesize=(612.0, 792.0))
    pdf.setFont("Times-Bold", 18)
    # Add data to the PDF
    pdf.drawString(50, 700, "Trip Information:")

    pdf.setFont("Times-Roman", 12)

    trips_dropped = len(response["dropped_trips"])
    total_trips = response["total_trips"]
    pdf.drawString(50, 650, f"Trips dropped ({trips_dropped}/{total_trips}):")
    text_object = pdf.beginText(50, 630)
    for trip in response["dropped_trips"]:
        text_object.textLine(trip)
    # Draw the text object to the canvas
    pdf.drawText(text_object)

     # Display each route
    y_position = 400
    for i, route in enumerate(response["routes"], start=1):
        pdf.setFont("Times-Bold", 12)
        # Display route title
        pdf.drawString(50, y_position, f"Route {i}:")
        y_position -= 20
        pdf.setFont("Times-Roman", 12)
        # Display route locations as a paragraph
        pdf.setFont("Helvetica", 10)
        text_object = pdf.beginText(50, y_position)
        
        line = ''
        counter = 0
        for id in route:
            line += id + ', '
            if counter == 8:
                text_object.textLine(line)
                counter = 0
                line = ''
        pdf.drawText(text_object)
        if line:
            text_object.textLine(line)  # Add the remaining IDs if any

    # Save the PDF to the specified file
    pdf.save()


def main():
    
    with open('../test_data/response.pkl', 'rb') as f:
        data = pickle.load(f)
    file_name = 'test.pdf'
    data["total_trips"] = 86
    # Create the PDF
    create_pdf(file_name, data)

if __name__ == "__main__":
    main()