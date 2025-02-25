
import unittest
from datetime import datetime
from app.models import review, place, user, BaseModel, amenitie


class TestModels(unittest.TestCase):

    def test_review(self):
        review_instance = review("Hello there !", 3, self.place, self.user)
        self.assertEqual(review_instance.text, "Hello there !")
        self.assertEqual(review_instance.rating, 5)
        self.assertEqual(review_instance.place, self.place)
        self.assertEqual(review_instance.user, self.user)

if __name__ == "__main__":
    unittest.main()