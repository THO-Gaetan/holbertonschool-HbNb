# test_create_place.py

from place import Place  # Assurez-vous que le fichier de la classe Place est bien importé
from data_management import DataManager

def test_create_place():
    """Teste la création d'un lieu et son enregistrement"""

    # Crée un objet Place avec des données fictives
    place_name = "Belle Villa"
    place_description = "Une magnifique villa avec vue sur la mer."
    place_location = "Côte d'Azur, France"
    owner_id = "12345"  # L'ID de l'utilisateur propriétaire, supposons qu'il existe

    # Crée une instance de la classe Place
    new_place = Place(name=place_name, description=place_description, location=place_location, owner_id=owner_id)

    # Affiche les informations du lieu créé pour vérifier qu'elles sont correctes
    print(f"Nom du lieu: {new_place.name}")
    print(f"Description du lieu: {new_place.description}")
    print(f"Emplacement du lieu: {new_place.location}")
    print(f"ID du propriétaire: {new_place.owner_id}")
    print(f"ID du lieu: {new_place.place_id}")
    print(f"Date de création: {new_place.created_at}")

    # Sauvegarde le lieu dans la base de données ou le fichier
    new_place.save_to_file()

    # Vérifie que le lieu a bien été ajouté (pour l'exemple, nous allons récupérer les lieux enregistrés)
    data_manager = DataManager()
    all_places = data_manager.get("places")  # Récupère tous les lieux enregistrés

    print("\n--- Liste des lieux enregistrés ---")
    for place_id, place_data in all_places.items():
        print(f"ID: {place_id}, Nom: {place_data['name']}, Emplacement: {place_data['location']}")

if __name__ == "__main__":
    test_create_place()
