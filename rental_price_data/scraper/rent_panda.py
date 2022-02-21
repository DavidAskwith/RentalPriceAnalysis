from requests import get
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from ..listing import Listing
from .processor import sanitizer

def get_page_source():

    def scroll_listings(driver):
        SCROLL_PAUSE_TIME = 0.5

        SCROLL_CONTAINER_SELECTOR = "document.getElementsByClassName(\"profile-container\")[0]"
        SCROLL_HEIGHT_SELECTOR = f"{SCROLL_CONTAINER_SELECTOR}.scrollHeight"
        # Get scroll height
        last_height = driver.execute_script(f"return {SCROLL_HEIGHT_SELECTOR}")

        while True:
            # Scroll down to bottom
            driver.execute_script(f"{SCROLL_CONTAINER_SELECTOR}.scrollTo(0, {SCROLL_HEIGHT_SELECTOR});")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(f"return {SCROLL_HEIGHT_SELECTOR}")

            if new_height == last_height:
                break
            last_height = new_height


    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)

    driver.get("https://www.rentpanda.ca/")
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
            address = raw_listings[0].select(".property-title")[0].string
            price = raw_listings[0].div.h2.span.span.string
            utilities = raw_listings[0].select(".utilities")[0].b.string

            specification = raw_listings[0].select(".specification")[0].div
            beds =  specification.div.span.string.replace(" Bed", "")
            baths = specification.contents[1].span.string.replace(" Bath", "")
            unit_type = specification.contents[2].span.string

            listing = sanitizer.sanitize(Listing(address, price, utilities, beds, baths, unit_type))
            listings.append(listing)

        return listings

    html_soup = BeautifulSoup(page_source, 'html.parser')
    raw_listings = html_soup.find_all('div', class_='top-section')

    listings = get_listings(raw_listings)
    return listings
