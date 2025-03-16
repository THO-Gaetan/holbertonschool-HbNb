# Define the places dictionary at the module level
places = {}

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenitie
from app.extensions import db
from sqlalchemy.orm import validates

# Define the association table for the many-to-many relationship
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    
    # Define the relationships
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place')
    amenities = db.relationship('Amenitie', secondary=place_amenity, back_populates='places')

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

def create_place(title, description, price, latitude, longitude, owner):
    place = Place(title, description, price, latitude, longitude, owner)
    places[place.id] = place
    owner.add_place(place)
    return place
