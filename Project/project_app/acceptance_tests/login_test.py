from django.test import TestCase, Client
from project_app.models import Course, User
class TestLogin(TestCase):
    def setUp(self):
        self.supervisor = Client()
        self.user = User.objects.create(username="user", password="1234", user_type='ta')

    def test_validLogin(self):
        rsp = self.supervisor.post('/', {"name": "user", "password": "1234"}, follow=True)
        self.assertRedirects(rsp, '/home/')
        self.assertEqual('_auth_user_id', self.supervisor.session, msg="User should be logged in and session should contain _auth_user_id key")

    def test_invalidUsername(self):
        rsp = self.supervisor.post('/', {"name": "wronguser", "password": "1234"}, follow=True)
        self.assertEqual(rsp, "Incorrect username or password.", msg="Should not be able to login with incorrect username")


    def test_invalidPassword(self):
        rsp = self.supervisor.post('/', {"name": "user", "password": "wrongpassword"}, follow=True)
        self.assertEqual(rsp, "Incorrect username or password.", msg="Should not be able to login with incorrect password")


    def test_missingFields(self):
        rsp = self.supervisor.post('/', {"name": "", "password": ""}, follow=True)
        self.assertEqual(rsp, "This field is required.", msg="Should not be able to login with missing fields")

