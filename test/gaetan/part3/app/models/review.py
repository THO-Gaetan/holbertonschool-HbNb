#!/usr/bin/python3
reviews = {}

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from app.extensions import db
from sqlalchemy.orm import validates


class Review(BaseModel):

    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Define the relationship
    user = db.relationship('User', back_populates='reviews')
    place = db.relationship('Place', back_populates='reviews')

    @validates('text')
    def validate_text(self, key, text):
        if not text:
            raise ValueError("Text cannot be empty")
        return text
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

def create_review(text, rating, user, place):
    review = Review(text, rating, user, place)
    reviews[review.id] = review
    place.add_review(review)
    return review