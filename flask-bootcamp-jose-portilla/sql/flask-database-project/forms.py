
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddPuppieForm(FlaskForm):

    name = StringField('Name of Puppy: ')
    submit = SubmitField('Add Puppy')


class DelForm(FlaskForm):

    id = IntegerField("ID Number of Puppy to Remove: ")
    submit = SubmitField("Remove Puppy")


class AddOwnerForm(FlaskForm):

    name = StringField('Name of Owner: ')
    id = IntegerField("ID of Puppy: ")
    submit = SubmitField("Add Owner")
