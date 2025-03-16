amenities = {}

from app.models.base_model import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates

class Amenitie(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(255), unique=True, nullable=False)

    # Define the relationship
    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty")
        return name


def create_amenity(name):
    amenity = Amenitie(name)
    amenities[amenity.id] = amenity
    return amenity
