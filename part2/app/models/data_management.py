import json

class DataManager:
    """Gère la persistance des données dans un fichier JSON"""
    
    def __init__(self, file_name="data.json"):
        """Initialise le gestionnaire de données avec un fichier.
        
        Cette méthode essaie d'ouvrir et de lire le fichier JSON existant, 
        ou crée un fichier vide si le fichier n'existe pas encore. 
        Elle charge les données du fichier dans l'attribut `self.data`.

        Args:
            file_name (str): Nom du fichier JSON utilisé pour stocker les données (par défaut "data.json").
        """
        self.file_name = file_name
        
        # Si le fichier n'existe pas, crée un fichier vide
        try:
            with open(self.file_name, 'r') as f:
                self.data = json.load(f)  # Charge les données existantes
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}  # Si fichier manquant ou erreur JSON, initialise un dictionnaire vide

    def save(self, category, item, item_id):
        """Sauvegarde un élément dans le fichier JSON sous une catégorie.
        
        Cette méthode permet d'ajouter un élément dans une catégorie spécifique (comme "users", "places", etc.)
        dans le fichier JSON. Si la catégorie n'existe pas, elle est créée.

        Args:
            category (str): La catégorie dans laquelle l'élément sera stocké (ex: "users").
            item (dict): L'élément à ajouter sous la forme d'un dictionnaire.
            item_id (str): L'identifiant unique de l'élément à sauvegarder.
        """
        if category not in self.data:
            self.data[category] = {}  # Si la catégorie n'existe pas, crée une nouvelle catégorie
        
        self.data[category][item_id] = item  # Ajoute l'élément à la catégorie sous l'ID spécifié
        
        self._save_to_file()  # Sauvegarde les données dans le fichier

    def get(self, category):
        """Récupère tous les éléments d'une catégorie.
        
        Cette méthode retourne tous les éléments d'une catégorie spécifiée. Si la catégorie n'existe pas, 
        un dictionnaire vide est retourné.

        Args:
            category (str): La catégorie à récupérer (ex: "users").

        Returns:
            dict: Tous les éléments de la catégorie spécifiée.
        """
        return self.data.get(category, {})  # Retourne les éléments de la catégorie, ou un dictionnaire vide

    def update(self, category, item, item_id):
        """Met à jour un élément dans la catégorie spécifiée.
        
        Cette méthode permet de mettre à jour un élément existant dans la catégorie spécifiée en utilisant son ID.
        Si l'élément n'existe pas, elle affiche un message d'erreur.

        Args:
            category (str): La catégorie de l'élément à mettre à jour (ex: "users").
            item (dict): Les nouvelles données de l'élément à mettre à jour.
            item_id (str): L'ID de l'élément à mettre à jour.
        """
        if category in self.data and item_id in self.data[category]:
            self.data[category][item_id] = item  # Met à jour l'élément
            self._save_to_file()  # Sauvegarde les données mises à jour
        else:
            print(f"Erreur : L'élément avec l'ID {item_id} n'existe pas dans la catégorie {category}")

    def delete(self, category, item_id):
        """Supprime un élément d'une catégorie.
        
        Cette méthode permet de supprimer un élément d'une catégorie spécifiée. 
        Elle retourne `True` si l'élément a été supprimé avec succès, et `False` si l'élément n'existe pas.

        Args:
            category (str): La catégorie de l'élément à supprimer (ex: "users").
            item_id (str): L'ID de l'élément à supprimer.

        Returns:
            bool: `True` si l'élément a été supprimé, `False` si l'élément n'existe pas.
        """
        if category in self.data and item_id in self.data[category]:
            del self.data[category][item_id]  # Supprime l'élément
            self._save_to_file()  # Sauvegarde les données après suppression
            return True  # Indique que la suppression a réussi
        return False  # Indique que l'élément n'a pas été trouvé

    def _save_to_file(self):
        """Sauvegarde les données dans le fichier JSON.
        
        Cette méthode est utilisée pour écrire les données actuelles dans le fichier JSON après chaque opération 
        de sauvegarde, mise à jour ou suppression.

        Elle garantit que les modifications sont persistées dans le fichier après chaque changement dans les données.
        """
        with open(self.file_name, 'w') as f:
            json.dump(self.data, f, indent=4)  # Sauvegarde les données sous forme de JSON avec une indentation de 4 espaces


    def find_user_by_email(self, email):
        """Recherche un utilisateur par son email dans le fichier JSON"""
        users = self.get("users")
        
        for user_id, user_data in users.items():
            if user_data.get("email") == email:
                return user_id, user_data  # Retourne l'ID et les informations de l'utilisateur
        return None, None  # Si l'email n'est pas trouvé
