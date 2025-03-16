from app.models import User, Place, Amenitie, Review
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.review_repository import ReviewRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_user(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)
    
    def update_users(self, user_id, user_data):
        return self.user_repo.update_user(user_id, user_data)

    def create_place(self, place_data):
        user = self.user_repo.get(place_data['owner_id'])
        if not user:
            raise ValueError("User not found")
        place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=user.id  # Use owner_id instead of owner
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return self.place_repo.update_place(place_id, place_data)
    
    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        try:
            self.place_repo.delete(place)  # Utilisez le repository pour supprimer la place
        except Exception as e:
            raise ValueError(f"An error occurred: {str(e)}")  # Soulever l'exception en cas d'erreur
        return {'message': 'Place successfully deleted'}  # Retourne un message de succès
    
    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        amenity = Amenitie(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Update an amenity and return the updated object or None if not found
        amenitie = self.amenity_repo.get(amenity_id)
        if not amenitie:
            return None
        return self.amenity_repo.update_amenitie(amenity_id, amenity_data)
    
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user or not place:
            raise ValueError("User or Place not found")
        # Correctly initialize the Review object using keyword arguments
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=user.id,
            place_id=place.id
        )
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return self.review_repo.update_review(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        review.place.reviews.remove(review)
        return review
    
    def get_review_count_by_user_place(self, user_id, place_id):
        return len([
            review for review in self.review_repo.get_all() 
            if isinstance(review, Review) and review.user.id == user_id and review.place.id == place_id
        ])
