import os
from sqlalchemy import Column, String, Integer, ARRAY, create_engine, Enum, DateTime
from flask_sqlalchemy import SQLAlchemy
import pymysql
from simplecrypt import encrypt, decrypt

key = "$2JTu&ovEs@Ysk$"

def encryption(code):
    secret_text=encrypt(key, code)
    encode = " ".join(map(str, secret_text))
    return encode

def decryption(code):
    decode = list(map(int, code.split(" ")))
    plaintext = decrypt(key, bytes(decode))

    return str(plaintext, 'utf-8')


database_name = "Work India"
username = 'root'
password = 'workindia'
host = 'localhost:3306'
database_path = "mysql+pymysql://{}:{}@{}/{}".format(
    username, password, host, database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
    db.create_all()

    

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def details(self):
        return {
            'id': self.id,
            'username': self.username,
            "password": self.password
        }

    def get_user_id(self):
        return {
            'userId': self.id,
        }

    def __repr__(self):
        return '<User %r>' % self.id

class Password(db.Model):
    __tablename__ = 'passwords'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    website = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(10000), nullable=False)
    user_id = Column(Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id,website,username,password):
        encPassword = encryption(password)
        self.password = encPassword
        self.user_id = user_id
        self.username = username
        self.website  = website

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def details(self):
        return {
            'id': self.id,
            'username': self.username,
            'website' : self.website,
            'password': decryption(self.password)
        }

    def __repr__(self):
        return '<Note %r>' % self.id