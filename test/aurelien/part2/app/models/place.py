import json
from base_model import BaseModel
from data_management import DataManager

class Place:
    """Gère les informations des lieux (hébergements)

    Attributs :
        places {}: Dictionnaire contenant les informations des lieux
    """

    places = {}

    def __init__(self, name, description, location, owner_id):
        """Méthode qui initialise l'instance de la classe Place

        Arguments :
            name (string): nom du lieu
            description (string): description du lieu
            location (string): emplacement géographique du lieu
            owner_id (int): ID de l'utilisateur propriétaire du lieu
        """

        self.stamps = BaseModel()  # Crée une instance de la classe BaseModel pour gérer les timestamps
        self.place_id = self.stamps.id  # Associe un identifiant unique au lieu
        self.name = name  # Nom du lieu
        self.description = description  # Description du lieu
        self.location = location  # Localisation géographique
        self.owner_id = owner_id  # ID de l'utilisateur propriétaire
        self.created_at = str(self.stamps.created_at)  # Date de création du lieu (timestamp)

    def to_dict(self):
        """Crée un dictionnaire avec toutes les informations du lieu"""

        data = {
            "name": self.name,  # Nom du lieu
            "description": self.description,  # Description du lieu
            "location": self.location,  # Localisation
            "owner_id": self.owner_id,  # ID du propriétaire
            "created_at": self.created_at  # Date de création
        }
        return data

    def save_to_file(self):
        """Sauvegarde les informations du lieu dans un fichier JSON"""

        data_manager = DataManager()  # Crée une instance de DataManager pour gérer la persistance des données
        existing_places = data_manager.get("places")  # Récupère la liste des lieux existants

        if self.place_id in existing_places:  # Vérifie si le lieu existe déjà
            return "Place already exists"  # Retourne un message si le lieu existe déjà

        data_manager.save("places", self.to_dict(), self.place_id)  # Sauvegarde les informations du lieu

    def place_update(self):
        """Met à jour les informations du lieu dans le fichier JSON"""

        data_manager = DataManager()

        # Crée un dictionnaire de données pour le lieu (par exemple, à partir de self)
        place_data = self.to_dict()

        # Appelle la méthode update sur DataManager en lui passant les bons arguments
        data_manager.update("places", place_data, self.place_id)  # Met à jour les informations du lieu
        print(f"Les informations du lieu avec l'ID {self.place_id} ont été mises à jour.")

    @classmethod
    def update_place_by_id(cls, place_id, new_data):
        """Met à jour un lieu par ID avec de nouvelles données"""

        data_manager = DataManager()

        # Récupérer les lieux existants
        places = data_manager.get("places")

        if place_id not in places:
            print(f"Aucun lieu trouvé avec l'ID : {place_id}")
            return False

        # Met à jour le lieu avec les nouvelles données
        place_data = places[place_id]
        place_data.update(new_data)  # Met à jour les champs du lieu avec new_data

        # Adapter les clés du dictionnaire place_data pour correspondre aux noms des arguments dans Place
        updated_place_data = {
            'name': place_data.get('name', ''),
            'description': place_data.get('description', ''),
            'location': place_data.get('location', ''),
            'owner_id': place_data.get('owner_id', ''),
        }

        # Créer un objet Place avec les nouvelles données
        place = cls(**updated_place_data)  # Instancier un lieu avec les données mises à jour
        place.place_id = place_id  # Assigner l'ID du lieu

        # Appeler la méthode place_update pour sauvegarder les changements
        place.place_update()

        print(f"Le lieu avec l'ID {place_id} a été mis à jour.")
        return True

    def delete_place(self):
        """Supprime les informations du lieu dans le fichier JSON"""

        data_manager = DataManager()  # Crée une instance de DataManager
        place_delete_result = data_manager.delete("places", self.place_id)  # Supprime le lieu de la base de données des lieux
        if not place_delete_result:
            print(f"Erreur : L'ID {self.place_id} n'a pas été trouvé dans 'places'.")

        return place_delete_result  # Retourne le résultat de la suppression du lieu
