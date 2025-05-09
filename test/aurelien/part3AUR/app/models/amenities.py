from app.models.basemodel import BaseModel
from app.Extension import db

class Amenitie(BaseModel):
    __tablename__ = 'amenities'
    
    id = db.Column(db.Integer, primary_key=True)  # Définition de la clé primaire
    _name = db.Column(db.String(100), nullable=False, unique=True)  # Définir l'attribut name dans la base de données
    
    

    def __repr__(self):
        return f"<Amenitie {self.name}>"

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    def to_dict(self):
        """Convert the amenity object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name
        }
