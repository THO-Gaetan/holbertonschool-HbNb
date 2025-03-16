from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'last_name': fields.String(required=True, description='Last name of the user'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """admin requests to register a new user"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        user_data = api.payload

        data = request.json
        email = data.get('email')
        
        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            # Simulate email uniqueness check (to be replaced by real validation with persistence)
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'last_name': new_user.last_name, 'first_name': new_user.first_name, 'email': new_user.email}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_user()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'password': user.password} for user in users], 200


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
    
@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    """Admin requets to update a user's information"""
    @api.expect(user_model, validate=True)
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """admin requests to update a user's information"""
        current_user = get_jwt_identity()
        
        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        """update a user's information"""
        user_data = api.payload
        try:
            updated_user = facade.update_users(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        