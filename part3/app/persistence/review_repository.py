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
    
    def update_review(self, review_id, data):
        review = self.get(review_id)
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            db.session.commit()
            return review
        return None
    
    def delete(self, review):
        db.session.delete(review)
        db.session.commit()
