from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify


def admin_required(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()  # Récupère l'identité de l'utilisateur à partir du JWT
            if not current_user.get('is_admin'):  # Si l'utilisateur n'est pas administrateur
                return jsonify(error="Admin privileges required"), 403  # Erreur 403
            return fn(*args, **kwargs)  # Appel de la fonction avec les arguments
        return decorated_function