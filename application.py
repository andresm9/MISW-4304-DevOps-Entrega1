from flask import Flask
from flask_restful import Resource, Api

application = Flask(__name__)
api = Api(application)

class Prueba(Resource):
    def get(self):
        return {'message': 'Prueba Endpoint siguiendo el Tutorial de AWS BeanStalk'}

api.add_resource(Prueba, '/prueba')

if __name__ == '__main__':
    application.run(debug=True)