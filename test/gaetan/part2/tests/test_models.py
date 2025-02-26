import unittest
from datetime import datetime
from app.models import Review, Place, User, BaseModel, Amenitie

# Import the create functions from their respective modules
from app.models.users import create_user
from app.models.places import create_place
from app.models.reviews import create_review
from app.models.amenities import create_amenity

class TestModels(unittest.TestCase):

    def test_methods(self):
        # Test User creation
        user = create_user("John Doe", "test@example.com")
        self.assertEqual(user.email, "test@example.com", "User email doesn't match")
        print("User creation test passed")

        # Test Place creation and relationship with User
        place = create_place("Cozy Cabin", "A beautiful cabin in the woods", 100.0, 40.7128, -74.0060, user)
        self.assertEqual(place.owner, user, "Place owner doesn't match")
        self.assertIn(place, user.places, "Place not in user's places")
        print("Place creation and User relationship test passed")

        # Test Review creation and relationship with Place and User
        review = create_review("Great place!", 5, user, place)
        self.assertIn(review, place.reviews, "Review not in place's reviews")
        self.assertEqual(review.user, user, "Review user doesn't match")
        self.assertEqual(review.place, place, "Review place doesn't match")
        print("Review creation and relationships test passed")

        # Test Amenity creation and relationship with Place
        amenity = create_amenity("Wi-Fi")
        place.add_amenity(amenity)
        self.assertIn(amenity, place.amenities, "Amenity not in place's amenities")
        print("Amenity creation and Place relationship test passed")

        print("All tests passed successfully!")

if __name__ == "__main__":
    unittest.main()