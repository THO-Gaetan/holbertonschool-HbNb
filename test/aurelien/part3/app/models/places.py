# Define the places dictionary at the module level
places = {}

from app.models.basemodel import BaseModel
from app.models.users import User
from app.models.amenities import Amenitie


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
        self.owner_id = owner.id

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value: str):
        if not value:
            raise ValueError("Title cannot be empty")
        self._title = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value: str):
        if not value:
            raise ValueError("Description cannot be empty")
        self._description = value
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        self._price = value
    
    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value: float):
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value: float):
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value
    
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value: User):
        if not isinstance(value, User):
            raise ValueError("Owner must be a User object")
        self._owner = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        """Convert the place object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            },
            'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in self.reviews],
            'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in self.amenities]
        }
        
    @property
    def owner_id(self):
        """Retourne l'ID du propriétaire du lieu"""
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        """Définir l'ID du propriétaire"""
        if value is None:
            raise ValueError("Owner ID cannot be None")
        self._owner_id = value

def create_place(title, description, price, latitude, longitude, owner):
    place = Place(title, description, price, latitude, longitude, owner)
    places[place.id] = place
    owner.add_place(place)
    return place
