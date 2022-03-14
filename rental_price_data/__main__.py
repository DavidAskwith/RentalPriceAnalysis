from .scraper import rent_panda
import csv
from datetime import datetime

source = rent_panda.get_page_source()
listings = rent_panda.scrape(source)

now = datetime.now()
nowFormatted = now.strftime("%d%m%Y")

with open(f"./data/RentalData_{nowFormatted}.csv", "w",) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["address", "price", "utilities", "beds", "baths", "unit_type", "ward", "coordinates"])
    for listing in listings:
        writer.writerow([listing.address, listing.price, listing.utilities, listing.beds, listing.baths, listing.unit_type, listing.ward, listing.coordinates])