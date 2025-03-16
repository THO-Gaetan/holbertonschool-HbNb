#!/usr/bin/python3
from app.extensions import bcrypt
from app.extensions import db
import re
from .base_model import BaseModel
from sqlalchemy.orm import validates

class User(BaseModel):
    """
    Classe représentant un utilisateur dans l'application.
    Hérite de BaseModel pour les fonctionnalités communes.
    """
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def verify_password(self, password: str) -> bool:
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self._password, password)

    def hash_password(self, value: str):
        """
        Setter pour le mot de passe de l'utilisateur.
        Hache le mot de passe en utilisant bcrypt.
        """
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')

    @validates('password')
    def validate_password(self, key, password):
        if not password or len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        return password

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not first_name or len(first_name) > 50:
            raise ValueError("Le prénom est requis et ne doit pas dépasser 50 caractères.")
        if len(first_name) == 0:
            raise ValueError("Le prénom ne peut pas être vide.")
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not last_name or len(last_name) > 50:
            raise ValueError("Le nom de famille est requis et ne doit pas dépasser 50 caractères.")
        if len(last_name) == 0:
            raise ValueError("Le nom de famille ne peut pas être vide.")
        return last_name
    
    @validates('email')
    def validate_email(self, key, email):
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Format d'email invalide.")
        if len(email) == 0:
            raise ValueError("L'email ne peut pas être vide.")
        return email
