import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'auregaKey')  # Clé secrète pour signer les JWT
    
    DEBUG = False
    # Paramètre de Flask-SQLAlchemy qui sert à désactiver ou
    # activer le suivi des modifications d'objets dans la
    # base de données.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Base de données de développement
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'auregaKey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    ENVIRONMENT = 'development'
    
class OnlineConfig(Config):
    DEBUG = False
    # Base de données pour l'environnement en ligne via 
    # une variable d'environnement
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://username:password@localhost:5000/hbnb_db')
ENVIRONMENT = 'online'
    
class TestingConfig(Config):
    TESTING = True
    # Base de données de test
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    ENVIRONMENT = 'testing'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'online': OnlineConfig,
    'testing': TestingConfig
}
