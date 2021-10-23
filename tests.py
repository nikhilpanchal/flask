from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    """
    Test cases for the User Model
    """
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_follow(self):
        """
        Testing the follow and unfollow capabilities
        """
        # Given
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        
        # Add the users to the db
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # Check the followed and followers for the case where none are setup
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        # Make user1 follow user2
        # When
        u1.follow(u2)
        db.session.commit()

        # Then
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        # Break the follow relationship
        # When
        u1.unfollow(u2)
        db.session.commit()

        # Then
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    
    def test_follow_posts(self):
        """
        Checks on the queries on the posts of the users being followed
        """
        # Given
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1,u2,u3,u4])

        now = datetime.utcnow()
        p1 = Post(body="Post from John", author=u1, timestamp=now+timedelta(seconds=1))
        p2 = Post(body="Post from Susan", author=u2, timestamp=now+timedelta(seconds=4))
        p3 = Post(body="Post from Mary", author=u3, timestamp=now+timedelta(seconds=3))
        p4 = Post(body="Post from David", author=u4, timestamp=now+timedelta(seconds=2))
        db.session.add_all([p1,p2,p3,p4])

        # When
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        db.session.commit()

        # Then
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)