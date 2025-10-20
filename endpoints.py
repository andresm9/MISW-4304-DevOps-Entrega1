import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models import Blacklist, db, BlackListRequestSchema


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Endpoint(Resource):
    def get(self):
        return {"message": "Blacklist Uniandes V4 (Inmmutable) - Grupo Nestor Andres Martinez, Juan Alberto Tapia, Sergio Andres Gelvez y Alberto Silva Rueda"},200


class Blacklists(Resource):

    @jwt_required()
    def post(self):

        try:

            # crear esquema para validar datos de entrada
            request_data = BlackListRequestSchema()
            data = request_data.load(request.json)

            logger.info("Request data", data)

            #Si el email ya fue agregado, retornar bad request
            if Blacklist.query.filter_by(email=data['email']).first():
                return {'message': 'Email Already Blacklisted'}, 400
            else:

                # agregar email a la blacklist
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
            # verificar si el email está en la blacklist
            blacklist_entry = Blacklist.query.filter_by(email=email).first()

            # Si no existe, devolver False
            if not blacklist_entry:
                return jsonify({"exist": False})

            # Si existe, devolver True y la razón del bloqueo
            return jsonify({"exist": True,"blocked_reason": blacklist_entry.blocked_reason})

        except Exception as e:
            return {'message': str(e)}, 400
