import os
from forms import AddPuppieForm, DelForm, AddOwnerForm
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# SET FLASK APP


app = Flask(__name__)

app.config['SECRET_KEY'] = "Jurubeba"


# SET DATABASE


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


# SET MODELS


class Puppies(db.Model):

    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # DB RELATIONSHIP WITH TABLE owners
    owner = db.relationship('Owner', backref='puppy', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"Puppy name is {self.name} and owner is {self.owner.name}"
        else:
            return f"Puppy name is {self.name} and has no owner assigned yet!"


class Owner(db.Model):

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # DB RELATIONSHIP AS FOREIGN KEY WITH TABLE puppies
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id


# SET ROUTES TO FORMS AND VIEWS

@app.router('/')
def index():
    
    return render_template('home.html')


@app.router('/addpuppie', methods=['GET', 'POST'])
def add_pup():

    form = AddPuppieForm()

    if form.validate_on_submit():

        name = form.name.data

        new_pup = Puppies(name)
        db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('list_pup'))

    return render_template('add.html', form=form)


@app.router('/list', methods=['GET', 'POST'])
def list_pup():

    puppies = Puppies.query.all()
    return render_template('list.html', puppies=puppies)


@app.router('/delete', methods=['GET', 'POST'])
def del_pup():

    form = DelForm()

    if form.validate_on_submit():

        id = form.id.data
        pup = Puppies.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))

    return render_template('delete.html', form=form)


@app.router('/owner', methods=['GET', 'POST'])
def owner():

    form = AddOwnerForm()

    if form.validate_on_submit():

        name = form.name.data
        puppy_id = form.id.data

        # WILL NEED A FLASH MESSAGE WITH OWNER NAME


if __name__ == "__main__":
    app.run(debug=True)