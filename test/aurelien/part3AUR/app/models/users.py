from app.Extension import db
from werkzeug.security import generate_password_hash, check_password_hash
import re 
from app.models.basemodel import BaseModel


class User(BaseModel):
    """
    Classe représentant un utilisateur dans l'application.
    Ce modèle est basé sur SQLAlchemy.
    """

    __tablename__ = 'users'  # Définir le nom de la table dans la base de données

    id = db.Column(db.String(36), primary_key=True)  # La clé primaire
    first_name = db.Column(db.String(50))  # Prénom de l'utilisateur
    last_name = db.Column(db.String(50))   # Nom de famille
    email = db.Column(db.String(120), unique=True)  # Email unique
    _password = db.Column(db.String(255))  # Mot de passe (stocké de façon sécurisée)
    is_admin = db.Column(db.Boolean, default=False)  # Drapeau indiquant si l'utilisateur est admin
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Date de création
    
    

    # Relations One-to-Many: Un utilisateur peut rédiger plusieurs avis
    

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

    @property
    def password(self) -> str:
        """Getter pour le mot de passe de l'utilisateur."""
        return self._password

    @password.setter
    def password(self, value: str):
        """
        Setter pour le mot de passe de l'utilisateur.
        Hache le mot de passe en utilisant bcrypt avant de le stocker dans la base de données.
        """
        if not value or len(value) < 8:
            raise ValueError("Le mot de passe doit avoir au moins 8 caractères.")
        self._password = generate_password_hash(value)

    @property
    def first_name(self) -> str:
        """Getter pour le prénom de l'utilisateur."""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        """
        Setter pour le prénom de l'utilisateur.
        Vérifie que le prénom n'est pas vide et ne dépasse pas 50 caractères.
        """
        if not value or len(value) > 50:
            raise ValueError("Le prénom est requis et ne doit pas dépasser 50 caractères.")
        self._first_name = value

    @property
    def last_name(self) -> str:
        """Getter pour le nom de famille de l'utilisateur."""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        """
        Setter pour le nom de famille de l'utilisateur.
        Vérifie que le nom n'est pas vide et ne dépasse pas 50 caractères.
        """
        if not value or len(value) > 50:
            raise ValueError("Le nom de famille est requis et ne doit pas dépasser 50 caractères.")
        self._last_name = value

    @property
    def email(self) -> str:
        """Getter pour l'adresse email de l'utilisateur."""
        return self._email

    @email.setter
    def email(self, value: str):
        """
        Setter pour l'adresse email de l'utilisateur.
        Vérifie que l'email a un format valide.
        """
        if not value or not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Format d'email invalide.")
        self._email = value

    def to_dict(self) -> dict:
        """Retourne un dictionnaire avec les informations de l'utilisateur."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at,
            "is_admin": self.is_admin
        }

    def verify_password(self, password: str) -> bool:
        """Vérifie si le mot de passe fourni correspond au mot de passe haché."""
        return check_password_hash(self.password, password)
