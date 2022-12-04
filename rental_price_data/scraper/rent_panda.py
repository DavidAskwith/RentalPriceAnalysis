from requests import get
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from ..listing import Listing
from .processor import sanitizer
from .processor import geodata
from .utilities import get_web_driver

def get_page_source():

    def scroll_listings(driver):
        SCROLL_PAUSE_TIME = 3

        SCROLL_CONTAINER_SELECTOR = "document.getElementsByClassName(\"profile-container\")[0]"
        SCROLL_HEIGHT_SELECTOR = f"{SCROLL_CONTAINER_SELECTOR}.scrollHeight"
        # Get scroll height
        last_height = driver.execute_script(f"return {SCROLL_HEIGHT_SELECTOR}")

        while True:
            # Scroll down to bottom
            # driver.execute_script(f"{SCROLL_CONTAINER_SELECTOR}.scrollTo(0, {SCROLL_HEIGHT_SELECTOR});")
            search_box = driver.find_element(By.CLASS_NAME, "listLoad").click()

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(f"return {SCROLL_HEIGHT_SELECTOR}")

            if new_height == last_height:
                break
            last_height = new_height

    driver = get_web_driver()
    driver.get("https://www.rentpanda.ca/search-result")

    # click thunder bay button
    search_box = driver.find_element(By.ID, "searchLocation")
    search_box.send_keys("Thunder Bay, ON, Canada")
    search_box.send_keys(Keys.RETURN)

    time.sleep(5)
    scroll_listings(driver)

    return driver.page_source

def scrape(page_source):

    def get_listings(raw_listings):
        listings = []

        for raw_listing in raw_listings:
            address = raw_listing.select(".property-title")[0].string
            price = sanitizer.get_numerical_price(raw_listing.div.h2.span.span.string)
            utilities = raw_listing.select(".utilities")[0].b.string

            specification = raw_listing.select(".specification")[0].div

            #handles case where room and baths don't exist for room only type
            first_spec =  specification.contents[0].span.string
            if first_spec != "Room for Rent":
                beds =  specification.contents[0].span.string.replace(" Bed", "")
                baths = specification.contents[1].span.string.replace(" Bath", "")
                unit_type = specification.contents[2].span.string
            else:
                beds = 0
                beths = 0
                unit_type = "Room"


            listing = Listing(address, price, utilities, beds, baths, unit_type)
            listing = geodata.update_listing_with_geodata(listing)
            listings.append(listing)

        return listings

    html_soup = BeautifulSoup(page_source, 'html.parser')
    raw_listings = html_soup.find_all('div', class_='top-section')

    listings = get_listings(raw_listings)
    return listings
