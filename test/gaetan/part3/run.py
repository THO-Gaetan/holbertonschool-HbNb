#!/usr/bin/env python3
from app import create_app, db
from app.models import User, Amenitie
from app.extensions import bcrypt

def insert_initial_data():
    app = create_app()
    with app.app_context():
        # Check if the admin user already exists
        admin_user = User.query.filter_by(email='admin@hbnb.io').first()
        if admin_user:
            print("Admin user already exists.")
            return

        # Create the admin user
        hashed_password = bcrypt.generate_password_hash('admin1234').decode('utf-8')
        admin_user = User(
            id='36c9050e-ddd3-4c3b-9731-9f487208bbc1',
            email='admin@hbnb.io',
            first_name='Admin',
            last_name='HBnB',
            password=hashed_password,
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user inserted successfully.")
if __name__ == "__main__":
    insert_initial_data()

def insert_initial_aminitie():
    app = create_app()
    with app.app_context():
        # Check if the admin user already exists
        existing_amenities = Amenitie.query.all()
        if existing_amenities:
            print("Aminities already exists.")
            return
        
        # Create the aminities
        new_aminitie = [
            Amenitie(name='Wifi'),
            Amenitie(name='Swimming_pool'),
            Amenitie(name='Air_conditioning')
        ]
        db.session.add_all(new_aminitie)
        db.session.commit()
        print("Aminities inserted successfully.")
if __name__ == "__main__":
    insert_initial_aminitie()
        
        
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
