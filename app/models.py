from datetime import datetime
from flask.helpers import url_for

from sqlalchemy.orm import backref
from app import db

"""
The followers association table. It's an association and not an entity table which is why it doesn't have
it's own class. Note also that it doesn't have any data of its own... purely made up of foreign keys
"""
followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

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


    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        """
        Return the most relevant posts made by users that this user (self) is following
        """
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(
            followers.c.follower_id == self.id
        )

        own = Post.query.filter_by(user_id = self.id)

        return followed.union(own).order_by(Post.timestamp.desc())


    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': datetime.now().isoformat() + 'Z',
            # 'about_me': self.about_me,
            'post_count': self.posts.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            '_links': {
                # url_for takes in the route handler function and will return the registered url with any 
                # prefixes
                'self': url_for('api.get_user', id=self.id),
                'followers': url_for('api.get_followers', id=self.id),
                'followed': url_for('api.get_followed', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])

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

