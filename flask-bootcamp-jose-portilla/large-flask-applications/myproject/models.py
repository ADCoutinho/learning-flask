# MODELS.PY - TOP LEVEL
# set up db inside the __init__.py under myproject folder

from myproject import db


class Puppies(db.Model):

    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # DB RELATIONSHIP WITH owners / 'uselist=False' as ONE TO ONE RELATION
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

    def __repr__(self):
        return f"Owner Name: {self.name}"
