from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Admin requests to register a new amenity"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'amenity': new_amenity.name}, 201
        except ValueError as e:
            return {'error': str(e)}, 400


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Placeholder for logic to return a list of all amenities
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'amenity': amenity.name} for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Placeholder for the logic to retrieve an amenity by ID
        amenities = facade.get_amenity(amenity_id)
        if not amenities:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenities.id, 'amenity': amenities.name}, 200
        
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Admin requests to update an amenity"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenities_data = api.payload

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenities_data)
            if updated_amenity is None:
                return {'error': 'Amenity not found'}, 404
            return {'message': 'Amenity updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        
        
@api.route('/amenities/<amenity_id>/places')
class Research(Resource):
    @api.response(200, 'List of places associated with an amenity retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get places associated with an amenity"""
        
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Récupérer les places associées à cet équipement
        places = amenity.places  # Grâce à la relation many-to-many

        # Retourner les données des places
        return [{'id': place.id, 'title': place.title, 'description': place.description} for place in places], 200