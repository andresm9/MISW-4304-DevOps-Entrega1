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

logger.info("RDS Database Hostname: %s", os.getenv('RDS_HOSTNAME', 'Not Set'))
logger.info("RDS Database Port: %s", os.getenv('RDS_PORT', 'Not Set'))
logger.info("RDS Database Name: %s", os.getenv('RDS_DB_NAME', 'Not Set'))
logger.info("RDS Database Username: %s", os.getenv('RDS_USERNAME', 'Not Set'))
logger.info("RDS Database password: %s", '********' if os.getenv('RDS_PASSWORD') else 'Not Set')

def create_app(test_config: dict | None = None):
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1440) # 60 days
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    with app.app_context():
        from models import db,ma
        from endpoints import Blacklists, Endpoint

        logger.info("Start Database...")
        db.init_app(app)
        ma.init_app(app)

        jwt = JWTManager(app)
        api = Api(app)
        cors = CORS(app, resources={r"/*": {"origins": "*"}})

        logger.info("Start API Endpoints...")
        api.add_resource(Endpoint, "/")
        api.add_resource(Blacklists, '/blacklists', '/blacklists/<string:email>')

        logger.info("Create Access Token...")
        try:

            access_token = create_access_token(identity="DefaultUser")
            logger.info("Access Token: %s", access_token)

        except:
            logger.debug("Access token creation skipped.")

    return app

if __name__ == '__main__':

    application = create_app()
    application.run(debug=False, use_reloader=False)