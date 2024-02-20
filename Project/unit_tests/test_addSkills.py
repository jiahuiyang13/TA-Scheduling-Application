from django.test import TestCase
from project_app.models import Course, User, Skill
from project_app.classes.ta import Ta

class TestAddSkills(TestCase):
    def setUp(self):
        self.ta= Ta()
        self.ta1 = User.objects.create(username="bob", password="bob", user_type="ta")#add skills to models
        self.ta2 = User.objects.create(username="pam", user_type="ta")
        self.admin = User.objects.create(username="suzie", password="bob", user_type="admin")
        self.skill = Skill.objects.create(owner=self.ta1, name="science")

    def test_Add(self):
        self.assertTrue(self.ta.addSkills("math", self.ta1.username), msg="skill should be added to list")
        found = list(Skill.objects.filter(name="math"))
        self.assertEquals(len(found), 1, msg="skill was not added to db")
        self.assertEquals(self.skill.owner, self.ta1, msg="should be a part of ta's skills now")

    def test_wrongUserType(self):
        self.assertFalse(self.ta.addSkills("math", self.admin.username), msg="admin type don't have skills")
        found = list(Skill.objects.filter(name="math"))
        self.assertEquals(len(found), 0, msg="skill should not be added to db")

    def tests_duplicateSkill(self):
        self.assertFalse(self.ta.addSkills("science", self.ta1.username), msg="duplicate skills should not be created")
        self.assertTrue(self.ta.addSkills("science", self.ta2.username), msg="other tas should be able to have same skill")

