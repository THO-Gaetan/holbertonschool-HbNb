![alt text](<hbnb3.jpg>)

# HBnB - Authentication & Database


HBNB est une application web inspirée d'Airbnb, permettant aux utilisateurs de rechercher et réserver des lieux de vacances. Développée avec Flask et SQLAlchemy, elle offre des fonctionnalités pour gérer les utilisateurs, lieux, équipements et avis.


## 1. Fonctionnalités principales
![alt text](bandeau.png)
__Gestion des utilisateurs__ : Inscription, modification, mise à jour et suppression de comptes d'utilisateur.

__Gestion des lieux__ : Création, mise à jour et suppression des lieux de vacances.

__Gestion des équipements__ : Ajouter des équipements spécifiques aux lieux (par exemple:  piscine, wifi).

__Gestion des avis__ : Permet aux utilisateurs de laisser des avis sur les lieux réservés.

__API RESTful__ : Interaction avec l'application via des endpoints API pour gérer les données.


## 2. Installation et lancement
![alt text](bandeau.png)
#### 2.1. Installation des dépendances

Clonez le dépôt et installez les dépendances nécessaires :
```
git clone https://github.com/votre-utilisateur/hbnb.git
cd hbnb
pip install -r requirements.txt
```

#### 2.2. Démarrage de l'application

Pour démarrer l'application en local, exécutez la commande suivante :
```
python3 run.py
```
Cela démarrera le serveur Flask sur http://localhost:5000.

## 3. Structure du projet
![alt text](bandeau.png)
#### 3.1. Dossier api/
Contient les routes API pour interagir avec les utilisateurs, les lieux, les équipements, et les avis.

* *__users.py__* : Routes pour gérer les utilisateurs.
* *__places.py__* : Routes pour gérer les lieux.
* *__amenities.py__* : Routes pour gérer les équipements.
* *__reviews.py__* : Routes pour gérer les avis.

#### 3.2. Dossier models/

Contient les modèles de données pour interagir avec la base de données via SQLAlchemy.

* *__user.py__* : Modèle pour l'utilisateur.
* *__place.py__* : Modèle pour le lieu.
* *__amenity.py__* : Modèle pour l'équipement.
* *__review.py__* : Modèle pour l'avis.

## 4. Utilisation de l'API
![alt text](bandeau.png)
#### 4.1. Authentification

L'API peut nécessiter une authentification basée sur un token JSON Web Token (JWT) . 

__Se connecter__ : L'utilisateur se connecte en envoyant ses identifiants (email et mot de passe) via une requête POST à l'endpoint /login.

__Obtenir le token__ : En cas de succès, l'API renvoie un token JWT qui contient les informations de l'utilisateur et est utilisé pour vérifier son identité dans les futures requêtes.


#### 4.2. EndPoints 
#### *Utilisateurs*

```GET /api/v1/users``` : Récupérer tous les utilisateurs.

```POST /api/v1/users``` : Créer un nouvel utilisateur.

```PUT /api/v1/users/users/{user_id}``` : Met à jour les informations d'un utilisateur via l'id 

```GET /api/v1/users/{user_id}``` : Récupère les détails d'un utilisateur via l'id


#### *Lieux*

```GET /api/v1/places``` : Récupérer tous les lieux.

```POST /api/v1/places``` : Créer un nouveau lieu.

```PUT /api/v1/places/places/{place_id}```:Met à jour les informations d'un lieu via l'id 

```GET /api/v1/places/places/{place_id}/amenities```:Récupère la liste des équipements associés à un lieu

```GET /api/v1/places/{place_id}```: Récupère les détails d'un lieu via l'id

```DELETE /api/v1/places/{place_id}```:Supprime un lieu via l'id


#### *Équipements*

```GET /api/v1/amenities``` : Récupérer tous les équipements.

```POST /api/v1/amenities``` : Ajouter un nouvel équipement.

```PUT /api/v1/amenities/amenities/{amenity_id}```:Met à jour les informations d'un équipement via l'id 

```GET /api/v1/amenities/amenities/{amenity_id}/places```: Récupère les lieux associés à un équipement via l'id 

```GET /api/v1/amenities/{amenity_id}```:Récupère les détails d'un équipement via l'id

#### *Avis*

```GET /api/v1/reviews``` : Récupérer tous les avis.

```POST /api/v1/reviews/```:Crée un nouvel avis pour un lieu

```GET /api/v1/reviews/places/{place_id}/reviews```: Récupère tous les avis associés à un lieu via l'id

```GET /api/v1/reviews/{review_id}```: Récupère les détails d'un avis spécifique via l'id 

```DELETE /api/v1/reviews/{review_id}```:Supprime un avis spécifique

```PUT /api/v1/reviews/{review_id}```: Met à jour un avis spécifique


#### *Auth*
```POST /api/v1/login```: Authentifie un utilisateur et génère un token JWT pour accéder aux ressources protégées.

```GET /api/v1/protected```:Accède à une ressource protégée, uniquement accessible avec un token valide.

## 5.Auteurs :
The project was developped by :
[![Anurag’s github stats](https://github-readme-stats.vercel.app/api?username=Aurelien292)](https://github.com/Aurelien292) ==> All the works
[Gaetan Pineiro](https://github.com/THO-Gaetan)
[![Anurag’s github stats](https://github-readme-stats.vercel.app/api?username=THO-Gaetan)](https://github.com/THO-Gaetan) ==> All the works
