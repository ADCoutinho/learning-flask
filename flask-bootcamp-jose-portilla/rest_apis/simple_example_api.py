import os
from flask import Flask
from flask_restful import Resource, Api
from werkzeug import generate_password_hash, check_password_hash
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jojoca'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(
    basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

api = Api(app)


#############################################

class Puppy(db.Model):

    __tablename__ = 'puppies'

    name = db.Column(db.String(80), primary_key=True)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name}


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __str__(self):
        return f"User Id: {self.id}"


#############################################

class PuppyNames(Resource):

    def get(self, name):

        pup = Puppy.query.filter_by(name=name).first()

        if pup:
            return pup.json()
        else:
            return {'name': None}, 404

    def post(self, name):

        pup = Puppy(name=name)
        db.session.add(pup)
        db.session.commit()

        return pup.json()

    def delete(self, name):

        pup = Puppy.query.filter_by(name=name).first()
        db.session.delete(pup)
        db.session.commit()

        return {'note': 'delete success'}


#############################################


def authenticate(username, password):
    # check if user exists
    # if so, return user
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)


jwt = JWT(app, authenticate, identity)


class AllNames(Resource):

    @jwt_required()
    def get(self):
        puppies = Puppy.query.all()

        return [pup.json() for pup in puppies]


api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames, '/puppies')


if __name__ == "__main__":
    app.run(debug=True)
