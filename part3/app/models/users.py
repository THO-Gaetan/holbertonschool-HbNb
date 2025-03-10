#!/user/bin/python3
import bcrypt
import re
from .basemodel import BaseModel
from .data_management import DataManager

class User(BaseModel):
    """
    Classe représentant un utilisateur dans l'application.
    Hérite de BaseModel pour les fonctionnalités communes.
    """

    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        """
        Initialise un nouvel utilisateur.

        :param first_name: Prénom de l'utilisateur
        :param last_name: Nom de famille de l'utilisateur
        :param email: Adresse email de l'utilisateur
        :param password: Mot de passe de l'utilisateur
        """
        super().__init__()  # Appel au constructeur de la classe parente pour gérer l'ID et la date de création
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # Utilise le setter pour valider et stocker le mot de passe
        self.created_at = str(self.created_at)  # Date de création générée automatiquement par BaseModel

    @property
    def password(self) -> str:
        """Getter pour le mot de passe de l'utilisateur."""
        return self._password

    @password.setter
    def password(self, value: str):
        """
        Setter pour le mot de passe de l'utilisateur.
        Hache le mot de passe en utilisant bcrypt.
        """
        if not value or len(value) < 8:
            raise ValueError("Le mot de passe doit avoir au moins 8 caractères.")
        salt = bcrypt.gensalt()  # Génération du sel pour bcrypt
        self._password = bcrypt.hashpw(value.encode('utf-8'), salt).decode('utf-8')

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
            "password": self.password,
            "created_at": self.created_at
        }

    def save_to_file(self) -> str:
        """Sauvegarde les informations de l'utilisateur dans un fichier JSON."""
        data_manager = DataManager()
        existing_emails = data_manager.get("emails")  # Vérifie si l'email existe déjà

        if self.email in existing_emails.values():
            return "Email already exists"
        
        data_manager.save("emails", self.email, self.user_id)  # Sauvegarde l'email
        data_manager.save("users", self.to_dict(), self.user_id)  # Sauvegarde les données complètes de l'utilisateur
        return "User saved successfully."

    def update_user(self) -> str:
        """Met à jour les informations de l'utilisateur dans le fichier JSON."""
        data_manager = DataManager()
        data_manager.update("users", self.to_dict(), self.user_id)  # Met à jour les informations de l'utilisateur
        return f"L'utilisateur avec l'ID {self.user_id} a été mis à jour."

    def delete_user(self) -> str:
        """Supprime un utilisateur et son email du fichier JSON."""
        data_manager = DataManager()
        
        # Supprime l'utilisateur
        if not data_manager.delete("users", self.user_id):
            return f"Erreur : L'utilisateur avec l'ID {self.user_id} n'a pas été trouvé."

        # Supprime l'email
        if not data_manager.delete("emails", self.user_id):
            return f"Erreur : L'email associé à l'utilisateur avec l'ID {self.user_id} n'a pas été trouvé."

        return f"L'utilisateur avec l'ID {self.user_id} a été supprimé avec succès."
