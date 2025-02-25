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

    # Si l'ID n'est pas trouvé, cela signifie que l'utilisateur n'existe pas
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
