import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')  # Clé secrète pour signer les JWT
    JWT_JSON_SERIALIZATION_ENABLED = True
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_TYPE = 'Bearer'
    DEBUG = False
    # Paramètre de Flask-SQLAlchemy qui sert à désactiver ou
    # activer le suivi des modifications d'objets dans la
    # base de données.

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENVIRONMENT = 'development'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENVIRONMENT = 'testing'

class ProductionConfig(Config):
    PRODUCTION = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENVIRONMENT = 'production'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
