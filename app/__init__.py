from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_recaptcha import ReCaptcha
from flask_caching import Cache
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
login = LoginManager()
recaptcha = ReCaptcha()
# cache = Cache()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    # cache.init_app(app)
    login.init_app(app)
    recaptcha.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_revoked(decoded_token):
        from app.utils.blacklist_helpers import is_token_revoked

        return is_token_revoked(decoded_token)

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app import models
