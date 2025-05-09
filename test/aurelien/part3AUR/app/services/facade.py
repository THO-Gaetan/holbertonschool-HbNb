from app.models.users import User
from app.models.places import Place
from app.models.amenities import Amenitie
from app.models.reviews import Review

from app.persistence.UserRepository import UserRepository
from app.persistence.PlaceRepository import PlaceRepository
from app.persistence.AmenityRepository import AmenityRepository
from app.persistence.ReviewRepository import ReviewRepository

class HBnBFacade:
    def __init__(self):
        # Utilisation de SQLAlchemyRepository pour chaque modèle
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # --- Utilisateur ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_user(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)
    
    def get_user_by_email(self, email):
        return self.user_repo.find_by_email(email)

    # --- Place ---
    def create_place(self, place_data, owner_id):
        user = self.user_repo.get(owner_id)
        if not user:
            raise ValueError("User not found")
        place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=user
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    # --- Amenity ---
    def create_amenity(self, amenity_data):
        amenity = Amenitie(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # --- Review ---
    def create_review(self, review_data, user_id):
        existing_review = self.review_repo.get_by_attribute('user_id', user_id)
        if existing_review and existing_review.place.id == review_data['place_id']:
            return existing_review
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user or not place:
            raise ValueError("User or Place not found")
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place,
            user_id=user_id
        )
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        review.place.reviews.remove(review)
        return review
