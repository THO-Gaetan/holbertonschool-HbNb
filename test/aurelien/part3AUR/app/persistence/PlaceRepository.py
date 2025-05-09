from app.models.places import Place
from app.Extension import db

class PlaceRepository:
    def __init__(self):
        self.model = Place  # Modèle Place pour le repository

    def create(self, title, description, price, latitude, longitude, owner):
        """Crée un nouveau lieu."""
        place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )
        db.session.add(place)
        db.session.commit()
        return place

    def get_by_id(self, place_id):
        """Récupère un lieu par son ID."""
        return Place.query.get(place_id)

    def get_all(self):
        """Récupère tous les lieux."""
        return Place.query.all()

    def update(self, place_id, **kwargs):
        """Met à jour un lieu existant."""
        place = self.get_by_id(place_id)
        if place:
            for key, value in kwargs.items():
                setattr(place, key, value)
            db.session.commit()
            return place
        return None

    def delete(self, place_id):
        """Supprime un lieu par son ID."""
        place = self.get_by_id(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
            return place
        return None
