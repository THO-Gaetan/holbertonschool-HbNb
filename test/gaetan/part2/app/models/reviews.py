#!/usr/bin/python3
reviews = {}

from app.models.users import User
from app.models.places import Place
from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

def create_review(text, rating, user, place):
    review = Review(text, rating, user, place)
    reviews[review.id] = review
    place.add_review(review)
    return review