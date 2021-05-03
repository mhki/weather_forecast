from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)  
    home = db.Column(db.String(100))
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(50), nullable=False)

class UserCity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, nullable=False)