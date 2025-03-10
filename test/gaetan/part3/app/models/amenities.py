amenities = {}

from app.models.basemodel import BaseModel

class Amenitie(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    def to_dict(self):
        """Convert the amenity object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name
        }

def create_amenity(name):
    amenity = Amenitie(name)
    amenities[amenity.id] = amenity
    return amenity
