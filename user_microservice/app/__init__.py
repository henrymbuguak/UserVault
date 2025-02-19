from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_caching import Cache
from flask_limiter.util import get_remote_address
from config import Config
import logging
import os
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['CACHE_TYPE'] = 'SimpleCache'  # Use Redis or Memcached in production
    cache.init_app(app)

     # Logging configuration
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microservice.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Microservice startup')

    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

        db.create_all()

    return app
