from app.models.basemodel import BaseModel
from app.models.users import User

from app.Extension import db
from app.models.basemodel import BaseModel

places = {}
# Table d'association pour la relation Many-to-Many Place <-> Amenity


class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Référence à l'utilisateur
    # Table d'association pour la relation Many-to-Many Place <-> Amenity
   
    
    
    def __repr__(self):
        return f"<Place {self.title}>"

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
    place = Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude, owner=owner)
    db.session.add(place)
    db.session.commit()
    return place
