from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jojoca'

api = Api(app)
jwt = JWT(app, authenticate, identity)

puppies = []


class PuppyNames(Resource):

    def get(self, name):

        for pup in puppies:
            if pup['name'] == name:
                return pup

        return {'name': None}, 404

    def post(self, name):

        pup = {'name': name}
        puppies.append(pup)

        return pup

    def delete(self, name):

        for ind, pup in enumerate(puppies):
            if pup['name'] == name:
                puppies.pop(ind)
                return {'note': 'delete success'}


class AllNames(Resource):

    @jwt_required()
    def get(self):
        return {'puppies': puppies}


api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames, '/puppies')


if __name__ == "__main__":
    app.run(debug=True)
