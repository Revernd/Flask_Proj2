import unittest
from app import create_app, db
from models import User


class TestURLs(unittest.TestCase):
    def setUp(self):
        app = create_app({
            'TESTING' : True,
            'SQLALCHEMY_DATABASE_URI' : 'sqlite:///tests\\test_database.db'
            })
        self.client = app.test_client()
        db.app = app
        db.create_all()

    def test_home_page(self):
         response = self.client.get('/')
         self.assertEqual(response.status_code, 200)
         self.assertIn(b'Hello World!!!', response.data)

    def tearDown(self):
         db.session.remove()
         db.drop_all()