from django.test import TestCase
from project_app.models import User
from project_app.classes.admin import Admin

class TestCreateAccount(TestCase):
    def setUp(self):
        self.admin_instance = Admin()
        self.account1 = User.objects.create(username="testuser1", password="testpass1", email="test1@example.com")
        self.account2 = User.objects.create(username="testuser2", password="testpass2", email="test2@example.com")

    def test_account_exists(self):
        self.assertFalse(self.admin_instance.create_account("testuser1", "testpass1", "test1@example.com"), msg='should have returned true since account is in db')

    def test_new_account(self):
        self.assertTrue(self.admin_instance.create_account("testuser3", "testpass3", "test3@example.com"), msg='should have added account and returned success msg')

    def test_invalid_username_type(self):
        with self.assertRaises(TypeError, msg="should raise exception for invalid username type"):
            self.admin_instance.create_account(38432489238, "testpass4", "test4@example.com")

class TestDeleteAccount(TestCase):
    def setUp(self):
        self.admin_instance = Admin()
        self.account1 = User.objects.create(username="testuser1", password="testpass1", email="test1@example.com")
        self.account2 = User.objects.create(username="testuser2", password="testpass2", email="test2@example.com")

    def test_account_exists(self):
        self.assertTrue(self.admin_instance.delete_account(self.account1.username), msg='should have returned true since account is in db')

    def test_no_account(self):
        self.assertFalse(self.admin_instance.delete_account('999'), msg='should have returned false since account is not in db')

    def test_invalid_input(self):
        with self.assertRaises(TypeError, msg="should raise exception for invalid input type"):
            self.admin_instance.delete_account(999)
