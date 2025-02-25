# Gestion des Utilisateurs

Ce projet permet de gérer des utilisateurs dans un système. Il contient plusieurs classes pour gérer les informations des utilisateurs (création, mise à jour, suppression, etc.) et la persistance de ces informations dans un fichier JSON.
Fonctionnalités
1. Classe BaseModel

Cette classe sert de modèle de base pour tous les objets qui nécessitent un identifiant unique et des timestamps. Elle permet de gérer les informations de date de création et de mise à jour des objets.
Attributs :

    id : Identifiant unique généré via uuid.
    created_at : Date de création (timestamp).
    updated_at : Date de dernière mise à jour (timestamp).

Méthodes :

    save() : Met à jour le champ updated_at.
    to_dict() : Retourne un dictionnaire des attributs de l'objet avec les timestamps formatés.

2. Classe User

La classe User permet de gérer les informations des utilisateurs, y compris l'enregistrement de leurs emails et mot de passe haché.
Attributs :

    emails : Liste des emails existants.
    user_places : Liste des lieux où l'utilisateur est hébergé.
    users : Dictionnaire contenant les utilisateurs.
    firstName : Prénom de l'utilisateur.
    lastName : Nom de l'utilisateur.
    email : Email de l'utilisateur.
    __password : Mot de passe de l'utilisateur, haché pour la sécurité.
    created_at : Date de création de l'utilisateur (timestamp).

Méthodes :

    __init__() : Initialise un utilisateur avec un prénom, un nom, un mot de passe et un email.
    hash_password() : Hache un mot de passe en utilisant la bibliothèque bcrypt.
    to_dict() : Retourne un dictionnaire contenant toutes les informations de l'utilisateur.
    save_to_file() : Sauvegarde l'utilisateur dans un fichier JSON. Vérifie si l'email existe déjà avant de sauvegarder.
    user_update() : Met à jour les informations de l'utilisateur dans le fichier JSON.
    delete_user() : Supprime l'utilisateur du fichier JSON ainsi que son email associé.

3. Classe DataManager

La classe DataManager gère la persistance des données dans un fichier JSON. Elle permet de sauvegarder, récupérer, mettre à jour et supprimer des éléments dans le fichier.
Attributs :

    file_name : Nom du fichier JSON utilisé pour stocker les données (par défaut "data.json").
    data : Contient les données chargées du fichier JSON.

Méthodes :

    __init__() : Charge les données du fichier JSON dans self.data ou crée un dictionnaire vide si le fichier n'existe pas.
    save(category, item, item_id) : Sauvegarde un élément dans une catégorie spécifique du fichier JSON.
    get(category) : Récupère tous les éléments d'une catégorie.
    update(category, item, item_id) : Met à jour un élément dans la catégorie spécifiée.
    delete(category, item_id) : Supprime un élément d'une catégorie.
    _save_to_file() : Sauvegarde les données dans le fichier JSON après chaque opération.

Structure du Fichier JSON

Le fichier JSON utilisé pour stocker les données a la structure suivante :

{
    "emails": {
        "2441a91c5c2d4988a580de0992220906": "johndoe@example.com"
    },
    "users": {
        "2441a91c5c2d4988a580de0992220906": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "$2b$12$JgVUlQAGyIMrPEVo7qCJQeshrJzfoA0fHZ.DROwU2dRse0LEqffqO",
            "created_at": "2025-02-24 10:30:30.795759"
        }
    }
}

    emails : Contient les emails des utilisateurs, où chaque email est associé à un identifiant unique (user_id).
    users : Contient les informations complètes des utilisateurs, identifiés par leur user_id.

## Exemple d'Utilisation - Creation et sauvegarde d'un utilisateur 
## fichier test


```
#!/usr/bin/python3
from user import User

# Création d'un nouvel utilisateur
user1 = User("John", "Doe", "password123", "johndoe@example.com")

# Sauvegarde de l'utilisateur
user1.save_to_file()

```

# Exemple d'Utilisation - Suppression d'un Utilisateur par Email
## fichier test

#!/usr/bin/python3

from user import User
from data_management import DataManager

# Fonction pour supprimer un utilisateur en utilisant son email
def delete_user_by_email(email_to_delete):
    # Crée une instance de DataManager pour gérer les données
    data_manager = DataManager()

    # Récupère la liste des utilisateurs
    users = data_manager.get("users")
    emails = data_manager.get("emails")

    # Recherche l'ID de l'utilisateur correspondant à l'email
    user_id_to_delete = None

    for user_id, user_data in users.items():
        if user_data['email'] == email_to_delete:
            user_id_to_delete = user_id
            break

    # Si l'ID n'est trouvé, cela signifie que l'utilisateur n'existe pas
    if user_id_to_delete is None:
        print(f"Aucun utilisateur trouvé avec l'email : {email_to_delete}")
        return

    # Crée un objet User pour l'utilisateur à supprimer
    user_data = users[user_id_to_delete]
    user1 = User(user_data['first_name'], user_data['last_name'], "dummy_password", user_data['email'])
    user1.user_id = user_id_to_delete  # Assigne l'ID à l'utilisateur pour effectuer la suppression

    # Supprime l'utilisateur et son email
    result = user1.delete_user()

    if result == (True, True):  # Vérifie que l'email et l'utilisateur ont bien été supprimés
        print(f"L'utilisateur avec l'email {email_to_delete} a été supprimé.")
    else:
        print(f"Erreur lors de la suppression de l'utilisateur avec l'email {email_to_delete}.")

if __name__ == "__main__":
    email_to_delete = "johndoe@example.com"  # Email de l'utilisateur à supprimer

    print("\n==== Suppression de l'utilisateur par email ====")
    delete_user_by_email(email_to_delete)  # Supprime l'utilisateur avec l'email spécifié


# Exemple d'Utilisation - Update d'un Utilisateur par Email 
## fichier test

#!/usr/bin/python3

from user import User

def test_update_user_by_email():
    email_to_update = "johndoe@example.com"  # Email de l'utilisateur à mettre à jour
    new_data = {
        "first_name": "Jonathan",
        "last_name": "Doe Jr.",
        "password": "newpassword123"  # Nouveau mot de passe
    }

    # Appeler la méthode pour mettre à jour l'utilisateur par email
    result = User.update_user_by_email(email_to_update, new_data)

    if result:
        print("L'utilisateur a été mis à jour avec succès.")
    else:
        print("La mise à jour a échoué.")

if __name__ == "__main__":
    test_update_user_by_email()