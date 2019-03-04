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
from app.models import User
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


user_fields = {
    'id': UUID,
    'name': fields.String,
    'email': fields.String,
}


# For testing
class AllUsers(Resource):
    def get(self):
        return marshal(User.query.all(), user_fields)

    def delete(self):
        for user in User.query.all():
            db.session.delete(user)
        db.session.commit()
        return {'msg': 'All user deleted'}


class UserDetail(Resource):
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

        resp['data'] = marshal(current_user, user_fields)
        return resp, 200


class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='Name not blank and must be string', required=True)
    parser.add_argument('email', type=str, help='Email not blank', required=True)
    parser.add_argument('password', type=str, help='Password not blank', required=True)

    def post(self):
        resp = dict(RESPONSE)
        args = self.parser.parse_args()
        exists_name = db.session.query(User.id).filter_by(name_lower=args['name'].lower()).scalar() is not None
        exists_email = db.session.query(User.id).filter_by(name_lower=args['email'].lower()).scalar() is not None

        if exists_name or exists_email:
            resp['msg'] = dict()
            resp['error'] = True
            if exists_name:
                resp['msg']['name'] = 'Username is already taken'
            if exists_email:
                resp['msg']['email'] = 'Email is already taken'
            return resp, 409

        current_user = User(
            name=args['name'],
            email=args['email']
        )
        current_user.set_password(password=args['password'])
        db.session.add(current_user)
        db.session.commit()

        resp['data'] = marshal(current_user, user_fields)
        resp['msg'] = f'User {current_user.name} was created'
        return resp, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='Name not blank and must be string', required=True)
    parser.add_argument('password', type=str, help='Password not blank', required=True)

    def post(self):
        resp = dict(RESPONSE)
        args = self.parser.parse_args()
        current_user = User.query.filter_by(name=args['name']).first()

        if current_user and current_user.check_password(args['password']):
            # Create our JWTs
            access_token = create_access_token(identity=current_user.id)
            refresh_token = create_refresh_token(identity=current_user.id)

            # Store the tokens in our store with a status of not currently revoked.
            add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
            add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])

            resp['access_token'] = access_token
            resp['refresh_token'] = refresh_token
            resp['msg'] = f'Logged in as {current_user.name}'
            return resp, 200

        resp['error'] = True
        resp['msg'] = 'Wrong username or password'
        return resp, 403


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        user_identity = get_jwt_identity()
        revoke_token(jti, user_identity)
        return {'message': 'Access token has been revoked'}, 200


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        user_identity = get_jwt_identity()
        revoke_token(jti, user_identity)
        return {'message': 'Refresh token has been revoked'}, 200
