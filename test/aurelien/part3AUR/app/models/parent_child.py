from app import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Parent(db.Model):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    children = relationship('Child', backref='parent', lazy=True)

class Child(db.Model):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)