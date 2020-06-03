# __ini__.py underneath myproject folder

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Atalaia'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(
    basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


# Register Blueprints
from myproject.puppies.views import puppies_blueprint
from myproject.owners.views import owners_blueprints

app.register_blueprint(owners_blueprints, url_prefix='/owners')
app.register_blueprint(puppies_blueprint, url_prefix='/puppies')
