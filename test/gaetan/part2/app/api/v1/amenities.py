from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # Placeholder for the logic to register a new amenity
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
        if not amenities:
            return {'error': 'Amenity not found'}, 404
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

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Placeholder for the logic to update an amenity by ID
        amenities_data = api.payload

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenities_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {'id': updated_amenity.id, 'amenity': updated_amenity.name}, 200
        except ValueError as e:
            return {'error': str(e)}, 400