from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin,db.Model):
    id= db.Column(db.Integer,primary_key=True)
    email= db.Column(db.String(150),unique=True)
    username= db.Column(db.String(150),unique=True)
    password= db.Column(db.String(150))
    date= db.Column(db.DateTime(timezone=True),default=func.now())
