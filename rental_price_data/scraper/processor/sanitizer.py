from rental_price_data.listing import Listing

def get_numerical_price(raw_price):
    return int(raw_price.replace('$', '').replace(',', ''))
