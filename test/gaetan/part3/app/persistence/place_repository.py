from app.persistence.repository import SQLAlchemyRepository
from app import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import Place # Import your models


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_place_by_id(self, place_id):
        return Place.query.filter_by(place_id=place_id).first()