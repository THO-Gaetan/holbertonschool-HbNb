from app.persistence.repository import SQLAlchemyRepository
from app import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import Amenitie  # Import your models


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenitie)

    def get_place_by_name(self, name):
        return Amenitie.query.filter_by(name=name).first()