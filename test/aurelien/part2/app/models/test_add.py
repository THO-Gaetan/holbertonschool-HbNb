#!/usr/bin/python3
from user import User

# Création d'un nouvel utilisateur
user1 = User("John", "Doe", "password123", "johndoe@example.com")

# Sauvegarde de l'utilisateur
user1.save_to_file()
