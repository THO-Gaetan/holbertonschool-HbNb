#!/usr/bin/python3

from app.models.basemodel import BaseModel

class review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        self.place.add_review(self)
