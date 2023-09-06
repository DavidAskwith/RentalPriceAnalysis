import re

from listing import Listing

def get_numerical_price(raw_price):
    return int(re.sub("[$,\s/a-zA-Z]", "", raw_price))
