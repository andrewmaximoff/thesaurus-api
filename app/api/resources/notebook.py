from flask import current_app as app
from flask_restful import (
    Resource,
    fields,
    marshal,
    reqparse
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_raw_jwt,
    get_jwt_identity,
)

from app import db
from app.models import User, Notebook
from app.utils.blacklist_helpers import (
    add_token_to_database,
    revoke_token
)
from app.utils.uuid_helpers import UUID

RESPONSE = {
    'data': None,
    'error': False,
    'msg': 'OK',
}

notebook_fields = {
    'id': UUID,
    'name': fields.String,
    'description': fields.String,
    'creation_date': fields.DateTime,
}


class NotebookDetail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='Name not blank and must be string', required=True)

    @jwt_required
    def get(self, notebook_id):
        resp = dict(RESPONSE)
        user_identity = get_jwt_identity()
        notebook = Notebook.query.filter_by(id=notebook_id, user_id=user_identity).first()
        if not notebook:
            resp['error'] = True
            resp['data'] = None
            resp['msg'] = f'Notebook {notebook_id} doesn\'t exists'
            return resp, 404

        resp['data'] = marshal(notebook, notebook_fields)
        return resp, 200

    @jwt_required
    def delete(self, notebook_id):
        resp = dict(RESPONSE)
        user_identity = get_jwt_identity()
        notebook = Notebook.query.filter_by(id=notebook_id, user_id=user_identity).first()
        if not notebook:
            resp['error'] = True
            resp['data'] = None
            resp['msg'] = f'Notebook {notebook_id} doesn\'t exists'
            return resp, 404

        db.session.delete(notebook)
        db.session.commit()
        resp['data'] = None
        resp['msg'] = f'Notebook has been deleted'
        return resp, 200

    @jwt_required
    def put(self, notebook_id):
        resp = dict(RESPONSE)
        args = self.parser.parse_args()
        user_identity = get_jwt_identity()
        notebook = Notebook.query.filter_by(id=notebook_id, user_id=user_identity).first()
        if not notebook:
            resp['data'] = None
            resp['msg'] = f'Notebook {notebook_id} doesn\'t exists'
            return resp, 404

        # Update if name has change
        if notebook.name != args['name']:
            notebook.name = args['name']
            db.session.commit()
        resp['data'] = marshal(notebook, notebook_fields)
        resp['msg'] = f'Notebook has been updated'
        return resp, 200


class NotebookList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='Name not blank and must be string', required=True)

    @jwt_required
    def get(self):
        resp = dict(RESPONSE)
        user_identity = get_jwt_identity()
        current_user = User.query.get(user_identity)
        if not current_user:
            resp['error'] = True
            resp['msg'] = f'User {user_identity} does\'t exists'
            resp['data'] = None
            return resp, 404

        notebooks = current_user.notebooks
        resp['data'] = marshal(notebooks, notebook_fields)
        return resp, 200

    @jwt_required
    def post(self):
        resp = dict(RESPONSE)
        args = self.parser.parse_args()
        user_identity = get_jwt_identity()
        current_user = User.query.get(user_identity)
        if not current_user:
            resp['error'] = True
            resp['msg'] = f'User {user_identity} does\'t exists'
            resp['data'] = None
            return resp, 404

        exists_name = db.session.query(User.id).filter_by(name_lower=args['name'].lower()).scalar() is not None
        if exists_name:
            resp['error'] = True
            resp['msg'] = f'Notebook with {args["name"]} name exists'
            resp['data'] = None
            return resp, 401

        notebook = Notebook(name=args['name'])
        notebook.user = current_user
        notebook.user_id = current_user.id
        db.session.add(notebook)
        db.session.commit()
        resp['data'] = marshal(notebook, notebook_fields)
        return resp, 200
