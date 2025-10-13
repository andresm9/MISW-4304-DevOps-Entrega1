import logging
import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_restful import Api

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Start Application")
application = Flask(__name__)
application.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1440) # 60 days
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with application.app_context():

    from endpoints import Blacklists, Endpoint
    from models import db, ma

    logger.info("Start Database...")
    db.init_app(application)
    db.drop_all()
    db.create_all()

    ma.init_app(application)

    jwt = JWTManager(application)
    api = Api(application)

    logger.info("Start API Endpoints...")
    api.add_resource(Endpoint, "/")
    api.add_resource(Blacklists, '/blacklists', '/blacklists/<string:email>')

    logger.info("Create Access Token...")
    access_token = create_access_token(identity="DefaultUser")
    logger.info("Access Token: %s", access_token)


if __name__ == '__main__':
    application.run(debug=False, use_reloader=False)