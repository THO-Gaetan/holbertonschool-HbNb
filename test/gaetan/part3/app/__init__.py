from flask import Flask
from flask_restx import Api
from app.extensions import bcrypt, jwt, db
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenity_ns
from app.api.v1.places import api as place_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns
from config import DevelopmentConfig, config



def create_app(config_class="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_class])
    app.config ['JWT_SECRET_KEY'] = 'aurtan'
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    environnment = app.config['ENVIRONMENT']
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API - {environnment} mode')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    return app