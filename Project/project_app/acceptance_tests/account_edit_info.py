from django.test import TestCase, Client
from project_app.models import User

class EditInfoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="userone", password="1234", name="userone",
                                        email="userone@example.com", phone="1234567890",
                                        address="123 Roadrage lane, Springfield, Illinois ", user_type="instructor")

    def test_editMyInfo_validField(self):
        self.client.post('/', {"name": "userone", "password": "1234"}, follow=True)
        response = self.client.post('/home/accountEdit/', {'user-fields': 'phone', 'newEntry': '0987654321'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '0987654321', msg="Phone number should be updated successfully")
        self.assertEqual(response.context['Message'], "Information updated successfully", msg="Invalid Message")

    def test_editMyInfo_invalidField(self):
        self.client.post('/', {"name": "userone", "password": "1234"}, follow=True)
        response = self.client.post('/home/accountEdit/', {'user-fields': 'invalidField', 'newEntry': 'newValue'})
        self.assertEqual(response.context['Message'], "Invalid field selected", msg="Invalid Message")

    def test_editMyInfo_noFieldProvided(self):
        self.client.post('/', {"name": "userone", "password": "1234"}, follow=True)
        response = self.client.post('/home/accountEdit/', {'user-fields': '', 'newEntry': 'newValue'})
        self.assertEqual(response.context['Message'], "Invalid field selected", msg="Invalid Message")
