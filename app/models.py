from datetime import datetime

from sqlalchemy.orm import backref
from app import db

class User(db.Model):
    """
    The Users table that holds details of the users on our app
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # To signify a relationship with the Post table
    # backref will be the name of the field added to instances of Post objects that will point
    # back to the instance of User that references it
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)


class Post(db.Model):
    """
    The Posts table to hold details of the posts that a user creates
    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # Note the default value of the next field is the utcnow function, and not the result of calling it ()
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.body)