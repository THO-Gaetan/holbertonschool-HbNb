import uuid
from app.extensions import db
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, func

class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = self.created_at
        self.updated_at = self.updated_at

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()