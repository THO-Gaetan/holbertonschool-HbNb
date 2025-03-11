#!/usr/bin/python3
reviews = {}

from app.models.basemodel import BaseModel
from app.models.users import User
from app.models.places import Place

class Review(BaseModel):
    def __init__(self, text, rating, user, place):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value: str):
        if not value:
            raise ValueError("Text cannot be empty")
        self._text = value
    
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value: int):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value: User):
        if not isinstance(value, User):
            raise ValueError("User must be a User object")
        self._user = value

    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value: Place):
        if not isinstance(value, Place):
            raise ValueError("Place must be a Place object")
        self._place = value
    
    def to_dict(self):
        """Convert the review object to a dictionary."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            },
            'place': {
                'id': self.place.id,
                'title': self.place.title,
                'description': self.place.description,
                'price': self.place.price,
                'latitude': self.place.latitude,
                'longitude': self.place.longitude
            }
        }

def create_review(text, rating, user, place):
    review = Review(text, rating, user, place)
    reviews[review.id] = review
    place.add_review(review)
    return review