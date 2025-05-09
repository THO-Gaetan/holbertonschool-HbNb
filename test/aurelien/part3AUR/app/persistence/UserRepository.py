from app.models.users import User
from app.Extension import db

class UserRepository:
    def __init__(self):
        self.model = User  # On définit le modèle avec lequel le repository interagira

    def add(self, user):
        """Ajoute un utilisateur à la base de données."""
        db.session.add(user)
        db.session.commit()

    def get(self, user_id):
        """Récupère un utilisateur par son ID."""
        return db.session.query(self.model).filter_by(id=user_id).first()

    def get_all(self):
        """Récupère tous les utilisateurs."""
        return db.session.query(self.model).all()

    def update(self, user_id, data):
        """Met à jour un utilisateur."""
        user = self.get(user_id)
        if user:
            user.update(data)
            db.session.commit()
        return user

    def delete(self, user_id):
        """Supprime un utilisateur."""
        user = self.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user
    @classmethod
    def get_user_by_email(email):
        """Retourne un utilisateur à partir de son email."""
        return User.query.filter_by(email=email).first()  

    def find_by_email(self, email):
        """Trouve un utilisateur par son adresse e-mail."""
        return db.session.query(self.model).filter_by(email=email).first()
