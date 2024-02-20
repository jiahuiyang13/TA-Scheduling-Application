from django.test import TestCase
from project_app.models import User, Skill
from project_app.classes.admin import Admin

class TestSearchUser(TestCase):
    def setUp(self):
        self.ta1 = User.objects.create(username="bob", user_type="ta")  # add skills to models
        self.ta2 = User.objects.create(username="pam", user_type="ta")
        self.skill = Skill.objects.create(owner=self.ta1, name="science")
        self.instructor = User.objects.create(username="alice", user_type="instructor")
        self.admin1 = Admin()

    def test_userExists(self):
        self.assertTrue(self.admin1.searchUser("bob"), msg='should have returned true since TA is in db')

    def test_noUser(self):
        self.assertFalse(self.admin1.searchUser("joe"), msg='should have returned false since TA is not in db')

    def test_invalidInput(self):
        with self.assertRaises(TypeError, msg="should raise exception for invalid search type"):
            self.admin1.searchUser(143)

    def test_invalidUserType(self):
        self.assertFalse(self.admin1.searchUser("alice"), msg="should not find user with user_type not ta")