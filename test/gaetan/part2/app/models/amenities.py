amenities = {}

from app.models.basemodel import BaseModel

class Amenitie(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
def create_amenity(name):
    amenity = Amenitie(name)
    amenities[amenity.id] = amenity
    return amenity