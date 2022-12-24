from requests import get
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from ..listing import Listing
from .processor import sanitizer
from .processor import geodata
import rental_price_data.config as config
from .utilities import get_web_driver

def get_raw_listings():

    def login(driver):
        email = driver.find_element(By.NAME, "email")
        email.send_keys(config.facebook_email)

        password = driver.find_element(By.NAME, "pass")
        password.send_keys(config.facebook_password)

        submit = driver.find_element(By.ID, "loginbutton")
        submit.click()

    def scroll_listings(driver):
        SCROLL_PAUSE_TIME = 3

        SCROLL_CONTAINER_SELECTOR = "document.querySelector('.x1glzykd.x1c4vz4f.xs83m0k')"
        SCROLL_HEIGHT_SELECTOR = f"{SCROLL_CONTAINER_SELECTOR}.scrollHeight"
        # Get scroll height
        last_height = driver.execute_script(f"return {SCROLL_HEIGHT_SELECTOR}")

        while True:
            # Scroll down to bottom
            driver.execute_script(f"window.scrollTo(0, {SCROLL_HEIGHT_SELECTOR});")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(f"return {SCROLL_HEIGHT_SELECTOR}")

            if new_height == last_height:
                break
            last_height = new_height

    def get_individual_listings_source(driver):
        listings_in_list = driver.find_elements(By.CSS_SELECTOR, ".xt7dq6l.xl1xv1r.x6ikm8r.x10wlt62.xh8yej3")

        raw_listings = []

        for listing_in_list in listings_in_list:
            listing_in_list.click()
            time.sleep(3)

            raw_html = driver.find_element(By.CSS_SELECTOR, ".x78zum5.x1iyjqo2.x1n2onr6.xdt5ytf").get_attribute("innerHTML")
            raw_listings.append(raw_html)
            driver.back()
            time.sleep(3)

        return raw_listings

    driver = get_web_driver(False)

    driver.get("https://www.facebook.com/marketplace/category/propertyrentals?exact=false&latitude=48.4175&longitude=-89.2645&radius=9")
    time.sleep(5)

    login(driver)
    time.sleep(5)

    scroll_listings(driver)

    return get_individual_listings_source(driver)


def scrape(page_sources):

    listings = []

    for page_source in page_sources:
        raw_listing = BeautifulSoup(page_source, 'html.parser')

        address = raw_listing.div.div.next_sibling.span.string
        price = sanitizer.get_numerical_price(raw_listing.div.div.div.div.span.string)
        utilities = None
        #here

        beds_baths_raw = ""
        beds =  specification.contents[0].span.string.replace(" Bed", "")
        baths = specification.contents[1].span.string.replace(" Bath", "")
        unit_type = specification.contents[2].span.string

        # Ancillary values
        title = raw_listing.div.h1.span.string

        listing = Listing(address, price, utilities, beds, baths, unit_type)
        listing = geodata.update_listing_with_geodata(listing)
        listings.append(listing)

    return listings
