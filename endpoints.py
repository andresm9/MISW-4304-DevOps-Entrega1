import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models import Blacklist, db, BlacklistSchema, BlackListRequestSchema


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Blacklists(Resource):

    @jwt_required()
    def post(self):

        try:

            logger.info("Received POST request to /blacklists")

            request_data = BlackListRequestSchema()
            data = request_data.load(request.json)

            logger.info("Request data", data)

            if Blacklist.query.filter_by(email=data['email']).first():
                return {'message': 'Email Already Blacklisted'}, 400
            else:
                new_blacklist = Blacklist()
                new_blacklist.email = data['email']
                new_blacklist.app_uuid = data['app_uuid']
                new_blacklist.blocked_reason = data['blocked_reason']
                new_blacklist.ip_address = request.remote_addr

                db.session.add(new_blacklist)
                db.session.commit()

                return {'message': 'Email Blacklisted Successfully'}, 201

        except Exception as e:
            return {'message': str(e)}, 400



    @jwt_required()
    def get(self, email):
        try:

            logger.info(f"Received GET request to /blacklists/{email}")

            blacklist_entry = Blacklist.query.filter_by(email=email).first()

            if not blacklist_entry:
                return jsonify({"exist": False})

            return jsonify({"exist": True,"blocked_reason": blacklist_entry.blocked_reason})

        except Exception as e:
            return {'message': str(e)}, 400
