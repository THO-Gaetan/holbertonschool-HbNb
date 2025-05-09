from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description='Liste des noms des équipements à associer à la place')
})
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload

        try:
            # Créer la place sans équipements pour l'instant
            new_place = facade.create_place(place_data)

            # Vérifier si des équipements sont fournis avec leurs IDs
            amenities_ids = place_data.get('amenities', [])
            
            if amenities_ids:
                # Récupérer les équipements en fonction de leurs IDs
                amenities = facade.get_by_ids(amenities_ids)

                # Filtrer les équipements valides (non None)
                valid_amenities = [amenity for amenity in amenities if amenity is not None]
                
                # Vérifier s'il y a des équipements invalides (non trouvés par ID)
                invalid_amenities = [amenity_id for amenity_id, amenity in zip(amenities_ids, amenities) if amenity is None]
                
                if invalid_amenities:
                    return {'error': f"The following amenity IDs were not found: {', '.join(invalid_amenities)}"}, 400

                # Si des équipements valides existent, les associer à la place
                if valid_amenities:
                    facade.add_amenities_to_place(new_place.id, valid_amenities)

            # Récupérer les équipements associés à la place après l'ajout
            place_amenities = [{'id': amenity.id, 'name': amenity.name} for amenity in new_place.amenities]

            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
                'amenities': place_amenities  # Liste des équipements associés à la place
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{'id': place.id,
                 'title': place.title,
                 'latitude': place.latitude,
                 'longitude': place.longitude} for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        places = facade.get_place(place_id)
        if not places:
            return {'error': 'Place not found'}, 404
        
        place_amenities = [{'id': amenity.id, 'name': amenity.name} for amenity in places.amenities]
        
        return {'id': places.id,
                'title': places.title,
                'description': places.description,
                'price': places.price,
                'latitude': places.latitude,
                'longitude': places.longitude,
                'owner': {
                    'id': places.owner.id,
                    'first_name': places.owner.first_name,
                    'last_name': places.owner.last_name,
                    'email': places.owner.email
                    },
                    'amenities': place_amenities
                }, 200

    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Admin or owner requests to delete a place"""
        current_user = get_jwt_identity()
        # Vérifiez si l'utilisateur est un administrateur ou le propriétaire de la place
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        # Suppression de la place
        try:
            facade.delete_place(place_id)  # Appelez la fonction pour supprimer la place
            return {'message': 'Place deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Admin requests to update a place's information"""
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Admin privileges required'}, 403

        place_data = api.payload

        try:
            updated_place = facade.update_place(place_id, place_data)
            if updated_place is None:
                return {'error': 'Place not found'}, 404
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/places/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get amenities associated with a place"""
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        
        # Récupérer les équipements associés à cette place
        amenities = place.amenities

        # Retourner les données des équipements
        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200