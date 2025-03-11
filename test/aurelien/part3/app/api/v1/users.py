from flask_restx import Namespace, Resource, fields, Api
from app.services import facade

from app.models import User
from flask_jwt_extended import create_access_token
from flask import request
import bcrypt


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'last_name': fields.String(required=True, description='Last name of the user'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Define the login model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        try:
            # Simulate email uniqueness check (to be replaced by real validation with persistence)
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'last_name': new_user.last_name, 'first_name': new_user.first_name, 'email': new_user.email,}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_user()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200
    
@api.route('/login')   
class UserLogin(Resource):
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    @api.response(400, 'Missing username or password')
    @api.expect(login_model, validate=True)
    def post(self):
        
        
        """Login and return a JWT token"""
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        if not email or not password:
            return {"msg": "Missing username or password"}, 400

        # Récupérer tous les utilisateurs
        users = facade.get_all_user()

        # Vérifier si l'email existe dans la liste des utilisateurs
        user = next((u for u in users if u.email == email), None)

        if not user:
            return {"msg": "Invalid credentials"}, 401

        # Vérifier le mot de passe haché avec bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Si le mot de passe est correct, créer un token JWT
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        else:
            return {"msg": "Invalid credentials"}, 401


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """update a user's information"""
        user_data = api.payload

        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        