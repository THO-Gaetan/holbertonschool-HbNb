from app.Extension import db
from app.models.reviews import Review

class ReviewRepository:
    def __init__(self):
        self.model = Review

    def add(self, review):
        """Ajoute une nouvelle review à la base de données"""
        db.session.add(review)
        db.session.commit()

    def get(self, review_id):
        """Récupère une review par son ID"""
        return db.session.query(self.model).get(review_id)

    def get_all(self):
        """Récupère toutes les reviews"""
        return db.session.query(self.model).all()

    def update(self, review_id, review_data):
        """Met à jour une review existante"""
        review = self.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        db.session.commit()
        return review

    def delete(self, review_id):
        """Supprime une review"""
        review = self.get(review_id)
        if not review:
            return None
        db.session.delete(review)
        db.session.commit()
        return review

    def get_by_user_and_place(self, user_id, place_id):
        """Récupère une review par l'utilisateur et le lieu"""
        return db.session.query(self.model).filter_by(user_id=user_id, place_id=place_id).first()
