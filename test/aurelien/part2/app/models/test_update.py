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