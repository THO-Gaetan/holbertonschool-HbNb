from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.models import Place


api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        
        current_user_id = get_jwt_identity()
        
        place = facade.get_place(review_data['place_id'])
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        if place.owner.id == current_user_id['id']:
            return {'error': 'Vous ne pouvez pas laisser une critique pour un lieu que vous possedez.'}, 400
        
        existing_review = facade.get_review_by_user_and_place(current_user_id['id'], review_data['place_id'])
        if existing_review:
            return {'error': 'Vous avez deja laisse une critique pour ce lieu.'}, 409

        try:
            new_review = facade.create_review(review_data, current_user_id)
            return {'id': new_review.id, 'text': new_review.text, 'rating': new_review.rating, 'user_id': new_review.user.id, 'place_id': new_review.place.id, 'owner_id': new_review.place.owner.id}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user.id, 'place_id': review.place.id}, 200

    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        
        current_user_id = get_jwt_identity()
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user.id != current_user_id['id']:
            return {'error': 'Unauthorized to modify this review'}, 403
        
        review_data = api.payload

        try:
            review = facade.update_review(review_id, review_data)
            if review is None:
                return {'error': 'Review not found'}, 404
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    
    def delete(self, review_id):
        """Delete a review"""
        
        current_user_id = get_jwt_identity()
    
        review = facade.delete_review(review_id)
        if review is None:
            return {'error': 'Review not found'}, 404
        if review.user.id != current_user_id['id']:
            return {'error': 'Unauthorized delete this review'}, 403
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [{'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user.id, 'place_id': review.place.id} for review in reviews], 200
