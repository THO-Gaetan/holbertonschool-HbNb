from app.persistence.repository import SQLAlchemyRepository
from app import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import Amenitie  # Import your models


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenitie)

    def get_place_by_name(self, name):
        return Amenitie.query.filter_by(name=name).first()
    
    def update_amenitie(self, amenitie_id, data):
        amenitie = self.get(amenitie_id)
        if amenitie:
            for key, value in data.items():
                setattr(amenitie, key, value)
            db.session.commit()
            return amenitie
        return None
    
    