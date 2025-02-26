users = {}

from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, name, email):
        super().__init__()
        self.name = name
        self.email = email
        self.places = []  
    
    def add_place(self, place):
        """Add a place to the user's owned places."""
        self.places.append(place)
