# Define the places dictionary at the module level
places = {}

from app.models.base_model import BaseModel
from app.models.users import User
from app.models.amenities import Amenitie
from app.extensions import db
from sqlalchemy.orm import validates, relationship

class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title cannot be empty")
        return title

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError("Description cannot be empty")
        return description

    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        return price
    
    @validates('latitude')
    def validate_latitude(self, key, latitude):
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude
    
    @validates('longitude')
    def validate_longitude(self, key, longitude):
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude
    
    @validates('owner_id')
    def validate_owner_id(self, key, owner_id):
        if not owner_id:
            raise ValueError("Owner ID cannot be empty")
        return owner_id

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

def create_place(title, description, price, latitude, longitude, owner):
    place = Place(title, description, price, latitude, longitude, owner)
    places[place.id] = place
    owner.add_place(place)
    return place
