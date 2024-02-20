from django.test import TestCase
from project_app.models import User
from project_app.classes.admin import Admin

class TestEditMyInfo(TestCase):
    def setUp(self):
        self.admin = Admin()
        self.user1 = User.objects.create(username="userone", password="1234", email="userone@example.com", address="123 Roadrage lane, Springfield, Illinois", phone="555-1234")
        self.user2 = User.objects.create(username="usertwo", password="4321", email="usertwo@example.com", address="1325 Barrington Rd, Hoffman Estates, IL 60169", phone="555-5678")

    def test_edit_info_success(self):
        result = self.admin.editInfo("userone", "555-4321", "userthree", "userthree@example.com", "987 New St, Springfield, Illinois")
        self.assertTrue(result, msg="error: Failed to update user information")

    def test_edit_info_duplicate_username(self):
        with self.assertRaises(ValueError, msg="Duplicate username, must raise error"):
            self.admin.editInfo("userone", "555-4321", "usertwo", "userone_modified@example.com",
                                "987 New St, Springfield, Illinois")

    def test_edit_info_duplicate_email(self):
        with self.assertRaises(ValueError, msg="Duplicate email, must raise error"):
            self.admin.editInfo("userone", "555-4321", "userone_modified", "usertwo@example.com",
                                "987 New St, Springfield, Illinois")

    def test_edit_info_invalid_username(self):
        with self.assertRaises(ValueError, msg="User not found in database, must raise error"):
            self.admin.editInfo("nonexistent_user", "555-4321", "userone_modified", "userone_modified@example.com",
                                "987 New St, Springfield, Illinois")

    def test_edit_info_invalid_input_type(self):
        with self.assertRaises(TypeError, msg="Invalid argument type, must raise error"):
            self.admin.editInfo("userone", 5554321, "userone_modified", "userone_modified@example.com",
                                "987 New St, Springfield, Illinois")

