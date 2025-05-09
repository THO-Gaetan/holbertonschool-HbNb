from flask_restx import Namespace, Resource
from app.models.parent_child import Parent

api = Namespace('parents', description='Operations related to parents and children')

@api.route('/')
class ParentList(Resource):
    def get(self):
        """List all parents with their children"""
        parents = Parent.query.all()
        result = []
        for parent in parents:
            children = [child.id for child in parent.children]
            result.append({'parent_id': parent.id, 'children': children})
        return result