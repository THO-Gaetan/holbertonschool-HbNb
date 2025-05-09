import os 
import logging
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenity_ns
from app.api.v1.places import api as place_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.auth import api as auth_ns
from config import config
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.Extension import db
from flask_migrate import Migrate


from app.models.parent_child import Parent, Child
from app.models.relationships import define_relationships



jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    app.config.from_object(config[config_name])
    
    
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    define_relationships()
    
    environnment = app.config['ENVIRONMENT']
    api = Api(app, version='1.0', title='HBnB API', description=f'HBnB Application API - {environnment} mode')
    
    
    from app.models import User
    from app.models import Place
    from app.models import Review
    from app.models import Amenitie
    
    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    return app