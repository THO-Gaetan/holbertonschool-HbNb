from app.persistence.repository import SQLAlchemyRepository
from app.extensions import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import Place # Import your models


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_place_by_id(self, place_id):
        return Place.query.filter_by(place_id=place_id).first()
    
    def update_place(self, place_id, data):
        place = self.get(place_id)
        if place:
            for key, value in data.items():
                setattr(place, key, value)
            db.session.commit()
            return place
        return None
    
    def delete(self, place):
        db.session.delete(place)
        db.session.commit()