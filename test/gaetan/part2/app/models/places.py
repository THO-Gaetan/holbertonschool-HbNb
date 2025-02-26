# Define the places dictionary at the module level
places = {}

from app.models.basemodel import BaseModel
from app.models.users import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

def create_place(title, description, price, latitude, longitude, owner):
    place = Place(title, description, price, latitude, longitude, owner)
    places[place.id] = place
    owner.add_place(place)
    return place
