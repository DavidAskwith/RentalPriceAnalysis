from rental_price_data.listing import Listing

def sanitize(listing):

    def sanitize_price(raw_price):
        return int(raw_price.replace('$', '').replace(',', ''))

    listing.price = sanitize_price(listing.price)
    return listing
