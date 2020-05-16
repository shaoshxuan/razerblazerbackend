from builtins import classmethod
from datetime import datetime

from app import *
from passlib.hash import pbkdf2_sha256 as sha256

db = get_db()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password,hash):
        return sha256.verify(password, hash)

    def __repr_(self):
        return '<User {}>'.format(self.email)

class UserProfile(db.Model):
    __tablename__ = 'userprofiles'
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer,db.ForeignKey('users.id'))
    mambuid = db.Column(db.String(100))
    encodedkey = db.Column(db.String(100))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    clientrolekey = db.Column(db.String(100))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<UserProfile {}>'.format(self.firstname,self.lastname)

class UserSubscriptions(db.Model):
    __tablename__ = 'usersubs'
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer,db.ForeignKey('users.id'))
    subname = db.Column(db.String(100))
    startdate = db.Column(db.DateTime, default=datetime.utcnow)
    nextpayment = db.Column(db.DateTime)
    enddate = db.Column(db.DateTime)
    subprice = db.Column(db.Integer)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()