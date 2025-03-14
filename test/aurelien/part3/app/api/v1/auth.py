from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade
from flask import jsonify

user_tokens = {}

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')  # Success response with code 200
    @api.response(401, 'Invalid credentials')  # Error response with code 401
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        
        user_tokens[user.id] = access_token
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200
    
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token ** Ne sert a rien ** """
        
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
         
        # Vérifier si le token est associé à l'utilisateur
        token = user_tokens.get(current_user['id'])
        if token:
            return jsonify(message=f"Hello, user {current_user['id']}. Your token is associated."), 200
        else:
            return jsonify(error="Token not found for user"), 401
    


@api.route('/administrator')
class Administrator(Resource):
    @api.expect(login_model)
    
    
    def post(self):
        
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        
        access_token = create_access_token(identity={'id': user.id, 'is_admin': True})
        print('\033[91mToken ADMIN\033[0m')
        return {'access_token': access_token}, 200
    
    
