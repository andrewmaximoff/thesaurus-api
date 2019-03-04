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
from app.models import User, Note, Notebook
from app.utils.blacklist_helpers import (
    add_token_to_database,
    revoke_token
)
from app.utils.uuid_helpers import UUID, uuid_param

RESPONSE = {
    'data': None,
    'error': False,
    'msg': 'OK',
}

note_fields = {
    'id': UUID,
    'name': fields.String,
    'description': fields.String,
    'creation_date': fields.DateTime,
}


class NoteDetail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='Name not blank and must be string', required=False)
    parser.add_argument('notebook_id', type=uuid_param, help='uuid not blank', required=False)

    @jwt_required
    def get(self, note_id):
        resp = dict(RESPONSE)
        user_identity = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_identity)
        if not note:
            resp['error'] = True
            resp['data'] = None
            resp['msg'] = f'Note {note_id} doesn\'t exists'
            return resp, 404

        resp['data'] = marshal(note, note_fields)
        return resp, 200

    @jwt_required
    def delete(self, note_id):
        resp = dict(RESPONSE)
        user_identity = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_identity).first()
        if not note:
            resp['error'] = True
            resp['data'] = None
            resp['msg'] = f'Note {note} doesn\'t exists'
            return resp, 404

        db.session.delete(note)
        db.session.commit()
        resp['data'] = None
        resp['msg'] = f'Note has been deleted'
        return resp, 200

    @jwt_required
    def put(self, note_id):
        resp = dict(RESPONSE)
        args = self.parser.parse_args()
        user_identity = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_identity).first()
        if not note:
            resp['data'] = None
            resp['msg'] = f'Note {note_id} doesn\'t exists'
            return resp, 404

        change = False

        if args['notebook_id']:
            notebook = Notebook.query.get(args['notebook_id'])
            if not notebook:
                resp['data'] = marshal(note, note_fields)
                resp['msg'] = f'Notebook {args["notebook_id"]} doesn\'t exists'
                return resp, 404
            elif note.notebook_id != args['notebook_id']:
                change = True
                note.notebook = notebook
                note.notebook_id = notebook.id

        if args['name']:
            if note.name != args['name']:
                change = True
                note.name = args['name']

        if change:
            db.session.commit()

        resp['data'] = marshal(note, note_fields)
        resp['msg'] = f'Note has been updated'
        return resp, 200


class NoteList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='Name not blank and must be string', required=True)
    parser.add_argument('description', type=str, help='Description must be string', required=False)
    parser.add_argument('notebook_id', type=uuid_param, help='uuid not blank', required=True)

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
        resp['data'] = marshal(notebooks, note_fields)
        return resp, 200

    @jwt_required
    def post(self):
        resp = dict(RESPONSE)
        args = self.parser.parse_args()
        user_identity = get_jwt_identity()
        current_user = User.query.get(user_identity)
        notebook = Notebook.query.get(args['notebook_id'])

        if not current_user:
            resp['error'] = True
            resp['msg'] = f'User {user_identity} does\'t exists'
            resp['data'] = None
            return resp, 404
        if not notebook:
            resp['error'] = True
            resp['msg'] = f'Notebook {user_identity} does\'t exists'
            resp['data'] = None
            return resp, 404

        note = Note(
            name=args['name'],
            description=args['description'],
        )
        note.user = current_user
        note.user_id = current_user.id
        note.notebook = notebook
        note.notebook_id = notebook.id
        db.session.add(note)
        db.session.commit()
        resp['data'] = marshal(note, note_fields)
        return resp, 200
