"""Définit la classe pour l'entité User (Utilisateur)"""
import bcrypt
from base_model import BaseModel
from data_management import DataManager


class User:
    """Gère les informations des utilisateurs

    Attributs :
        emails []: Contient tous les emails existants dans le système
        user_places []: Contient la liste des lieux que l'utilisateur héberge
        users {}: Dictionnaire contenant les informations de l'utilisateur
    """

    emails = []
    user_places = []
    users = {}

    def __init__(self, firstName, lastName, password, email):
        """Méthode qui initialise l'instance de la classe User

        Arguments :
            firstName (string): prénom de l'utilisateur
            lastName (string): nom de famille de l'utilisateur
            password (string): mot de passe de l'utilisateur
            email (string): email de l'utilisateur
        """

        self.stamps = BaseModel()  # Crée une instance de la classe BaseModel pour gérer les timestamps
        self.user_id = self.stamps.id  # Associe un identifiant unique à l'utilisateur
        self.firstName = firstName  # Prénom de l'utilisateur
        self.lastName = lastName  # Nom de famille de l'utilisateur
        self.__password = self.hash_password(password)  # Hash du mot de passe
        self.email = email  # Email de l'utilisateur
        self.created_at = str(self.stamps.created_at)  # Date de création de l'utilisateur (timestamp)
        

    def hash_password(self, password):
        """Hache un mot de passe en utilisant bcrypt.

        Arguments :
            password (string): le mot de passe en texte clair à hacher

        Retourne :
            string: le mot de passe haché
        """
        salt = bcrypt.gensalt()  # Génère un sel pour le hachage
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hache le mot de passe
        return hashed_password.decode('utf-8')  # Retourne le mot de passe haché sous forme de chaîne de caractères
    
    def to_dict(self):
        """Crée un dictionnaire avec toutes les informations de l'utilisateur
        """
        
        data = {
            "first_name": self.firstName,  # Prénom
            "last_name": self.lastName,  # Nom de famille
            "email": self.email,  # Email
            "password": self.__password,  # Mot de passe haché
            "created_at": self.created_at  # Date de création
        }
        return data
    
    def save_to_file(self):
        """Sauvegarde les informations de l'utilisateur dans un fichier JSON
        """
        
        data_manager = DataManager()  # Crée une instance de DataManager pour gérer la persistance des données
        existing_emails = data_manager.get("emails")  # Récupère la liste des emails existants

        if self.email in existing_emails.values():  # Vérifie si l'email existe déjà
            return "Email already exists"  # Retourne un message si l'email existe déjà
        
        data_manager.save("emails", self.email, self.user_id)  # Sauvegarde l'email de l'utilisateur
        data_manager.save("users", self.to_dict(), self.user_id)  # Sauvegarde les informations complètes de l'utilisateur

    def user_update(self):
    # Utilisation correcte de update en fonction des arguments requis
        data_manager = DataManager()

    # Crée un dictionnaire de données pour l'utilisateur (par exemple, à partir de self)
        user_data = self.to_dict()

    # Appelle la méthode update sur DataManager en lui passant les bons arguments
    # Assurez-vous que update attend trois arguments (resource, data, id)
    # self.user_id doit être l'ID de l'utilisateur que vous voulez mettre à jour
        data_manager.update("users", user_data, self.user_id)  # Met à jour les informations de l'utilisateur
        print(f"Les informations de l'utilisateur avec l'ID {self.user_id} ont été mises à jour.")
        
    @classmethod
    def update_user_by_email(cls, email, new_data):
        # Recherche l'utilisateur par email et met à jour ses informations

        data_manager = DataManager()

        # Récupérer les utilisateurs
        users = data_manager.get("users")

        user_id_to_update = None

        for user_id, user_data in users.items():
            if user_data["email"] == email:
                user_id_to_update = user_id
                break

        if user_id_to_update is None:
            print(f"Aucun utilisateur trouvé avec l'email : {email}")
            return False

        # Met à jour l'utilisateur avec les nouvelles données
        user_data = users[user_id_to_update]
        user_data.update(new_data)  # Mettre à jour les champs de l'utilisateur avec new_data
        
        # Adapter les clés du dictionnaire user_data pour correspondre aux noms des arguments dans User
        updated_user_data = {
        'firstName': user_data.get('first_name', ''),
        'lastName': user_data.get('last_name', ''),
        'email': user_data.get('email', ''),
        'password': user_data.get('password', ''),
        
    }
        
        # Si le mot de passe est mis à jour, on le hache avant de le stocker
        if 'password' in new_data:
            user = cls(**updated_user_data)  # Instancier un utilisateur avec les données mises à jour
            user_data['password'] = user.hash_password(new_data['password'])

        # Créer un objet User avec les nouvelles données
        user = cls(**updated_user_data)  # Instancier un utilisateur avec les données mises à jour
        user.user_id = user_id_to_update  # Assigner l'ID utilisateur

        # Appeler la méthode user_update pour sauvegarder les changements
        user.user_update()

        print(f"L'utilisateur avec l'email {email} a été mis à jour.")
        return True

    def delete_user(self):
        """Supprime les informations de l'utilisateur dans le fichier JSON
        """
        data_management = DataManager()  # Crée une instance de DataManager
        email_delete_result = data_management.delete("users", self.user_id)  # Supprime l'utilisateur de la base de données des utilisateurs
        if not email_delete_result:
            print(f"Erreur : L'ID {self.user_id} n'a pas été trouvé dans 'users'.")
        
        user_delete_result = data_management.delete("emails", self.user_id)  # Supprime l'email de la base de données des emails
        if not user_delete_result:
            print(f"Erreur : L'ID {self.user_id} n'a pas été trouvé dans 'emails'.")

        return email_delete_result, user_delete_result  # Retourne les résultats de la suppression de l'email et de l'utilisateur
    