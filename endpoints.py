from flask_jwt_extended import jwt_required
from flask_restful import Resource


class Blacklists(Resource):

    @jwt_required()
    def get(self):
        return {'message': 'Prueba Endpoint siguiendo el Tutorial de AWS BeanStalk'}