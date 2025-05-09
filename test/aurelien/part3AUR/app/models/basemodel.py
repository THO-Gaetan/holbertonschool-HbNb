from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Utilisation de la base de déclaration SQLAlchemy
Base = declarative_base()

class BaseModel(db.Model):
    __abstract__ = True  # Indique que ce modèle est abstrait et ne sera pas directement mappé en base

    # Définit les attributs communs pour tous les modèles
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def save(self):
        """Appelée pour enregistrer un objet et mettre à jour le `updated_at`."""
        self.updated_at = datetime.now(timezone.utc)
