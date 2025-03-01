from app.models import User, Place, Amenitie, Review, BaseModel
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_user(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        place = Place(**place_data)
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
        return self.place_repo.update(place_id, place_data)
    
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
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        return self.review_repo.delete(review_id)
