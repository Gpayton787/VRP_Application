import jinja2
import pdfkit


def create_pdf(raw_data, invalid_trips, date, response):
    trip_count = len(raw_data["trips_list"])
    invalid_trips = invalid_trips
    wcalls = raw_data["wcalls"]
    invalid_los = raw_data["invalid_los"]
    dropped_trips = len(response["dropped_trips"])
    routes = response["routes"]

    context = {
        "trip_count": trip_count,
        "dropped_trips": dropped_trips,
        "date": date,
        "wcalls": wcalls,
        "invalid_los": invalid_los,
        "invalid_trips": invalid_trips,
        "routes": routes,
    }

    templateLoader = jinja2.FileSystemLoader(searchpath="./pdf_creation")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "pdf_template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(outputText, 'output.pdf', configuration=config)


def main():
    pass