from app.models.amenities import Amenitie
from app.Extension import db

class AmenityRepository:
    def __init__(self):
        self.model = Amenitie  # Référence au modèle Amenitie

    def add(self, amenity):
        """Ajouter une nouvelle commodité"""
        db.session.add(amenity)
        db.session.commit()

    def get(self, amenity_id):
        """Récupérer une commodité par son ID"""
        return self.model.query.get(amenity_id)

    def get_all(self):
        """Récupérer toutes les commodités"""
        return self.model.query.all()

    def update(self, amenity_id, amenity_data):
        """Mettre à jour une commodité existante"""
        amenity = self.get(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            db.session.commit()
        return amenity

    def delete(self, amenity_id):
        """Supprimer une commodité par son ID"""
        amenity = self.get(amenity_id)
        if amenity:
            db.session.delete(amenity)
            db.session.commit()
        return amenity
