# Holberton School HBnB - Part 2

This project contains the implementation of a simple web application for managing users, places, reviews, and amenities. The application is built using Flask and Flask-RESTx for creating RESTful APIs. The project includes models, services, and API endpoints for managing the different entities.

## Directory Structure

```
part2/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── amenities.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/
│   │   ├── amenities.py
│   │   ├── basemodel.py
│   │   ├── places.py
│   │   ├── reviews.py
│   │   └── users.py
│   ├── persistence/
│   │   └── repository.py
│   └── services/
│       └── facade.py
├── tests/
│   └── test_models.py
├── run.py
└── requirements.txt
```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/THO-Gaetan/holbertonschool-HbNb.git
   cd holbertonschool-HbNb/part2
   ```

2. Create a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask application:
   ```sh
   ./run.py
   ```

2. The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Users

- **POST /users/**: Register a new user.
- **GET /users/**: Retrieve a list of all users.
- **GET /users/<user_id>**: Get user details by ID.
- **PUT /users/<user_id>**: Update a user's information.

### Places

- **POST /places/**: Register a new place.
- **GET /places/**: Retrieve a list of all places.
- **GET /places/<place_id>**: Get place details by ID.
- **PUT /places/<place_id>**: Update a place's information.

### Reviews

- **POST /reviews/**: Register a new review.
- **GET /reviews/**: Retrieve a list of all reviews.
- **GET /reviews/<review_id>**: Get review details by ID.
- **PUT /reviews/<review_id>**: Update a review's information.
- **DELETE /reviews/<review_id>**: Delete a review.
- **GET /places/<place_id>/reviews**: Get all reviews for a specific place.

### Amenities

- **POST /amenities/**: Register a new amenity.
- **GET /amenities/**: Retrieve a list of all amenities.
- **GET /amenities/<amenity_id>**: Get amenity details by ID.
- **PUT /amenities/<amenity_id>**: Update an amenity's information.

## Models

### User

The `User` model represents a user in the application. It includes attributes such as `first_name`, `last_name`, `email`, and `password`. The password is hashed using bcrypt.

### Place

The `Place` model represents a place in the application. It includes attributes such as `title`, `description`, `price`, `latitude`, `longitude`, and `owner`. It also includes methods to add reviews and amenities.

### Review

The `Review` model represents a review in the application. It includes attributes such as `text`, `rating`, `user`, and `place`.

### Amenitie

The `Amenitie` model represents an amenity in the application. It includes an attribute `name`.

### BaseModel

The `BaseModel` class provides common attributes and methods for all models, such as `id`, `created_at`, and `updated_at`.

## Testing

The `tests/test_models.py` file contains unit tests for the models. To run the tests, use the following command:

```sh
python3 -m unittest discover tests
```

## Authors

This project is the work of :

[Aurelien Goaoc](https://github.com/Aurelien292)\
[Gaetan Pineiro](https://github.com/THO-Gaetan)