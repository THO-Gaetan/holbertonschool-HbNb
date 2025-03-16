from app.persistence.repository import SQLAlchemyRepository
from app import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import User  # Import your models


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()  
    
    def update_user(self, user_id, data):
        user = self.get(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None