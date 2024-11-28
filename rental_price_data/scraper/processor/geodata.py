from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from ..scraper_error import ScraperError
import requests


from .wards import ward_polygons
from config import google_api_key


def update_listing_with_geodata(listing):

    def get_listing_geodata(listing):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={listing.address}&key={google_api_key}"
        r = requests.get(url)

        if r.status_code != 200:
            # todo log
            print(url)
            raise ScraperError("Geodata API Failure")

        geodata = r.json()

        if geodata["status"] == "ZERO_RESULTS":
            # todo log
            print(url)
            raise ScraperError("No Results Found")

        if geodata["status"] != "OK":
            # todo log
            print(url)
            raise ScraperError(geodata["error_message"])

        result = geodata["results"][0]
        return result


    def get_coordinates(geodata):
        lat = geodata["geometry"]["location"]["lat"]
        lng = geodata["geometry"]["location"]["lng"]
        return (lat, lng)

    def get_ward(coordinates):
        # swap cordinate ordeer since lat and long is in opposite order to the Point mapping
        point = Point(coordinates[1], coordinates[0])

        for key in ward_polygons:
            for poly in ward_polygons[key]:
                polygon = Polygon(poly)

                if polygon.contains(point):
                    return key
        return "OUTSIDE WARDS"


    geodata = get_listing_geodata(listing)
    listing.coordinates = get_coordinates(geodata)
    listing.ward = get_ward(listing.coordinates)
    listing.address = geodata["formatted_address"]

    return listing
