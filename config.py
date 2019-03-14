import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cache
    # CACHE_TYPE = 'redis'
    # CACHE_KEY_PREFIX = 'fcache'
    # CACHE_DEFAULT_TIMEOUT = 1*10*60

    # reCAPTCHA
    RECAPTCHA_ENABLED = True
    RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = os.getenv("JWT_BLACKLIST_ENABLED")
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
