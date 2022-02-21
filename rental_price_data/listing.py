class Listing:
  def __init__(self, address, price, utilities, beds, baths, unit_type, ward=None, cordinates=None):
    self.address = address
    self.price = price
    self.utilities = utilities
    self.beds = beds
    self.baths = baths
    self.unit_type = unit_type
    self.ward = ward
    self.cordinates = cordinates
