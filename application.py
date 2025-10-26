import logging
import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_restful import Api
from flask_cors import CORS

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(test_config: dict | None = None):

    logger.info("RDS Database Hostname: %s", os.getenv('RDS_HOSTNAME', 'Not Set'))
    logger.info("RDS Database Port: %s", os.getenv('RDS_PORT', 'Not Set'))
    logger.info("RDS Database Name: %s", os.getenv('RDS_DB_NAME', 'Not Set'))
    logger.info("RDS Database Username: %s", os.getenv('RDS_USERNAME', 'Not Set'))
    logger.info("RDS Database password: %s", '********' if os.getenv('RDS_PASSWORD') else 'Not Set')

    application = Flask(__name__)

    application.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1440)  # 60 days
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        application.config.update(test_config)
    else:
        logger.info("Setting up Database Connection...")

        if not os.getenv('RDS_HOSTNAME'):
            logger.warning("RDS_HOSTNAME not set")
            application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        else:
            logger.info("Using RDS configuration for database connection")
            database_uri = f"postgresql://{os.getenv('RDS_USERNAME')}:{os.getenv('RDS_PASSWORD')}@{os.getenv('RDS_HOSTNAME')}:{os.getenv('RDS_PORT')}/{os.getenv('RDS_DB_NAME')}"
            application.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    with application.app_context():
        from models import db, ma
        from endpoints import Blacklists, Endpoint

        logger.info("Start Database...")
        db.init_app(application)

        if test_config:
            logger.info("Testing Mode: Creating Mock SQL Tables...")
        else:
            logger.info("Creating PostgreSQL Tables...")
            db.create_all()

        ma.init_app(application)

        jwt = JWTManager(application)
        api = Api(application)
        cors = CORS(application, resources={r"/*": {"origins": "*"}})

        logger.info("Start API Endpoints...")
        api.add_resource(Endpoint, "/")
        api.add_resource(Blacklists, '/blacklists', '/blacklists/<string:email>')

        logger.info("Create Access Token...")
        try:

            access_token = create_access_token(identity="DefaultUser")
            logger.info("Access Token: %s", access_token)

        except:
            logger.debug("Access token creation skipped.")

    return application


"""if __name__ == '__main__':
    application = create_app()
    application.run(debug=False, use_reloader=False)
"""