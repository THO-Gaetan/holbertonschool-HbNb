#!/usr/bin/python3
import json
from place import Place

def delete_place(place_id):
    """Supprime un lieu du fichier data.json"""
    try:
        # Charger les lieux existants depuis le fichier JSON
        with open('data.json', 'r') as f:
            places = json.load(f)
        
        # Vérifier si le lieu existe et le supprimer
        if place_id in places:
            del places[place_id]  # Supprimer le lieu avec l'ID spécifié
            
            # Sauvegarder les lieux mis à jour dans le fichier JSON
            with open('data.json', 'w') as f:
                json.dump(places, f, indent=4)
            return True  # Indiquer que la suppression a réussi
        else:
            return False  # Indiquer que le lieu n'a pas été trouvé
    except FileNotFoundError:
        print("Erreur: Le fichier places.json n'existe pas.")
        return False
    except json.JSONDecodeError:
        print("Erreur: Le fichier places.json est corrompu.")
        return False
