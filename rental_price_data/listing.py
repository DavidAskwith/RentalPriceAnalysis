class Listing:
  def __init__(self, address, price, utilities, beds, baths, unit_type, ward=None, coordinates=None):
    # Core Values
    # Populated from all sites due to relevance in stat calculations
    self.address = address
    self.price = price
    self.utilities = utilities
    self.beds = beds
    self.baths = baths
    self.unit_type = unit_type
    if ward is None:
        self.ward = ward
    else:
        self.ward = ""

    if coordinates is None:
        self.coordinates = coordinates
    else:
        self.ward = ""

    # Ancillary Values
