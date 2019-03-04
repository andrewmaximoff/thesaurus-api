from flask import Blueprint
from flask_restful import Api

from app.api.resources.user import (
    UserRegistration,
    UserLogin,
    UserLogoutAccess,
    UserLogoutRefresh,
    UserDetail,
    AllUsers,
)
from app.api.resources.notebook import NotebookList, NotebookDetail
from app.api.resources.token import TokenRefresh


bp = Blueprint('api', __name__)
api = Api(bp)

# User endpoints
api.add_resource(AllUsers, '/user/test/')
api.add_resource(UserRegistration, '/user/registration/')
api.add_resource(UserLogin, '/user/login/')
api.add_resource(UserLogoutAccess, '/user/logout/access/')
api.add_resource(UserLogoutRefresh, '/user/logout/refresh/')
api.add_resource(UserDetail, '/user/me/')

# Note endpoints
api.add_resource(NotebookList, '/notebook/')
api.add_resource(NotebookDetail, '/notebook/<uuid:notebook_id>/')

# Token endpoints
api.add_resource(TokenRefresh, '/token/refresh/')
