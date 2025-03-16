from app.persistence.repository import SQLAlchemyRepository
from app import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import Review  # Import your models


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user(self, user_id):
        return Review.query.filter_by(user_id=user_id).all()
