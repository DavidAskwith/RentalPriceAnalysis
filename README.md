# Thunder Bay Rental Price Analysis
A utility used to scrape and analyze rental data. This tool will allow for weekly analysis of the rental market. The ward of the rental is determined using the address and Google Geocoding API.

## Motivation
Any data associated to rental in Thunder Bay is derived from a very small data set and is usually out of date. This results in inaccurate data.


## Install

Install `pipenv`

Run `pipenv install` in the `rental_price_data` directory

## Executing

Run `pipenv shell` to activate the virtual environment then run the module with `python rental_price_data`

## Technology

### Scraping
* Python
* Selenium
* BeutifulSoup

### Analysis
* Python
* Pandas
