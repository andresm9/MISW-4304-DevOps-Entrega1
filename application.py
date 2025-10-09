import os
import logging
from datetime import timedelta

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Start Application")
application = Flask(__name__)
application.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=72)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with application.app_context():

    from endpoints import Blacklists
    from models import db

    logger.info("Start Database...")
    db.init_app(application)
    db.create_all()

    jwt = JWTManager(application)
    api = Api(application)

    logger.info("Start API Endpoints...")
    api.add_resource(Blacklists, '/blacklists')

    logger.info("Create Access Token...")
    access_token = create_access_token(identity="DefaultUser")
    logger.info("Access Token: %s", access_token)


if __name__ == '__main__':
    application.run(debug=True)