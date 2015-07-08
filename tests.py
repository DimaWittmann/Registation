import os
import unittest
import json
from flask.ext.testing import TestCase as FlaskTestCase

from app import app, db, models

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        user = models.User(email="a@gmail.com", password="1111", other="")
        db.session.add(user)
        db.session.commit()

        user = models.User(email="f@gmail.com", password="1111", other="")
        db.session.add(user)
        db.session.commit()

        user = models.User(email="x@gmail.com", password="1111", other="")
        db.session.add(user)
        db.session.commit()

        user = models.User(email="b@gmail.com", password="1111", other="")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class ApiTest(BaseTestCase):

    def test_get_users(self):
        """
        Test that /api/users GET return users
        """
        response = self.app.get('/api/users')
        response = json.loads(response.data.decode("utf-8"))

        self.assertTrue(any(map(lambda x: x['email'] == "a@gmail.com", response['users'])))
        self.assertTrue(any(map(lambda x: x['email'] == "b@gmail.com", response['users'])))

    def test_get_sorted_by_email_users(self):
        response = self.app.get('/api/users?sort=email')
        response = json.loads(response.data.decode("utf-8"))['users']
        self.assertTrue(all(response[i]['email'] < response[i+1]['email']for i in range(0, len(response)-1)))

    def test_get_sorted_by_email_desc_users(self):
        response = self.app.get('/api/users?sort=-email')
        response = json.loads(response.data.decode("utf-8"))['users']
        self.assertTrue(all(response[i]['email'] > response[i+1]['email']for i in range(0, len(response)-1)))

    def test_get_sorted_by_date_desc_users(self):
        response = self.app.get('/api/users?sort=-date')
        response = json.loads(response.data.decode("utf-8"))['users']
        self.assertEqual(response[0]['email'], 'b@gmail.com')
        self.assertEqual(response[-1]['email'], 'a@gmail.com')

    def test_register_new_user_only_once(self):
        """
        Test that /api/users POST save user to db
        :return:
        """
        new_user = json.dumps({
            'email': 'd@gmail.com',
            'password': '1234'
        })
        number_of_users = models.User.query.count()

        response = self.app.post('/api/users', data=new_user,
                                 content_type='application/json')
        self.assertEqual(response._status_code, 201)

        response = self.app.post('/api/users', data=new_user,
                                 content_type='application/json')
        response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response['email'], ['Email already registered.'])

        response = self.app.get('/api/users')
        response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(len(response['users']), number_of_users + 1)

    def test_registration_with_empty_credentials(self):
        new_user = json.dumps({
            'email': '',
            'password': ''
        })
        number_of_users = models.User.query.count()
        response = self.app.post('/api/users', data=new_user,
                                 content_type='application/json')
        self.assertEqual(response._status_code, 400)
        self.assertEqual(number_of_users, models.User.query.count())

        response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response['email'], ['Email is required'])
        self.assertEqual(response['password'], ['Password is required'])

    def test_get_one_user(self):
        response = self.app.get('/api/users/1')
        response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response['user']['email'], "a@gmail.com")

    def test_get_non_existing_user(self):
        response = self.app.get('/api/users/100')
        self.assertEqual(response._status_code, 404)


class RegistrationPageTest(BaseTestCase):

    def test_registration_page_works(self):
        response = self.app.get('/').data.decode("utf-8")
        assert ("New user:" in response)

    def test_message_when_user_registered(self):
        response = self.app.post('/', data={
            'email': 'v@gmail.com',
            'password': '4321'
        }).data.decode('utf-8')
        self.assertIn('New user has been registered', response)

    def test_error_messages_when_empty_password(self):
        response = self.app.post('/', data={
            'email': 'v@gmail.com',
            'password': ''
        }).data.decode('utf-8')
        self.assertIn('Password is required', response)

    def test_error_messages_when_empty_email(self):
        response = self.app.post('/', data={
            'email': '',
            'password': '1212'
        }).data.decode('utf-8')
        self.assertIn('Email is required', response)

    def test_error_messages_when_user_email_isnt_unique(self):
        response = self.app.post('/', data={
            'email': 'a@gmail.com',
            'password': '123'
        }).data.decode('utf-8')
        self.assertIn('Email already registered', response)


if __name__ == '__main__':
    unittest.main()
