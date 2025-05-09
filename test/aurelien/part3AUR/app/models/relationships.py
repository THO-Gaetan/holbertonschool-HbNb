from app.Extension import db

def define_relationships():
    """
    Centralise toutes les relations entre les modèles.
    """
    
     # Relation One-to-Many: Un utilisateur peut créer plusieurs places, mais chaque place appartient à un seul utilisateur.
    from app.models.users import User
    from app.models.places import Place
    from app.models.reviews import Review
    from app.models.amenities import Amenitie

    User = db.relationship('User', backref='owner', lazy='subquery')
    Place = db.relationship('Place', backref='place', lazy='subquery')
    Review = db.relationship('Review', backref='author', lazy='subquery')

    # Relation Many-to-Many: Un lieu peut avoir plusieurs commodités, et chaque commodité peut être associée à plusieurs lieux.
    place_amenities = db.Table('place_amenities',
        db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
        db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True),
        extend_existing=True
    )
    Place.amenities = db.relationship('Amenitie', secondary=place_amenities, backref='places', lazy='subquery')
    Amenitie.places = db.relationship('Place', secondary=place_amenities, backref='amenities', lazy='subquery')