#!/usr/bin/python3
reviews = {}

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from app.extensions import db
from sqlalchemy.orm import validates


class Review(BaseModel):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)

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

    @validates('user_id')
    def validate_user_id(self, key, user_id):
        if not isinstance(user_id, User):
            raise ValueError("User must be a User object")
        return user_id

    @validates('place_id')
    def validate_place_id(self, key, place_id):
        if not isinstance(place_id, Place):
            raise ValueError("Place must be a Place object")
        return place_id
    
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