from django.test import TestCase, Client
from project_app.models import User, Skill

class TestCreateCourse(TestCase):
    supervisor = None
    thingList = None
    def setUp(self):
        self.supervisor = Client()
        self.validUser = User.objects.create(username="alidz", password="star", user_type="ta")
        self.validUser2 = User.objects.create(username="lucy", password="star", user_type="ta")
        self.invalidUser = User.objects.create(username="bob", password="star", user_type="prof")
        self.skill = Skill.objects.create(name="math", owner=self.validUser)

    def test_addSkill(self):
        self.supervisor.post('/', {"name": "alidz", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/addSkills/', {'newSkill': 'science', "name": "alidz"})
        self.assertEqual(rsp.context['Message'], "Success!", msg="skill should be added")
        self.assertEqual(list(Skill.objects.filter(owner=self.validUser)).__len__(), 2)
        self.assertEqual(rsp.context['mySkills'], [self.skill, Skill.objects.get(name='science')], msg="list should be updated with new item added")

    def test_invalidUser(self):
        self.supervisor.post('/', {"name": "bob", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/addSkills/', {'newSkill': 'science', "name": "alidz"})
        self.assertEqual(rsp.context['Message'], "Failed to add skill", msg="skill should not be added")
        self.assertEqual(list(Skill.objects.filter(owner=self.invalidUser)).__len__(), 0)
        self.assertEqual(rsp.context['mySkills'], [],msg="list should still be empty")

    def test_duplicateSkill(self):
        self.supervisor.post('/', {"name": "alidz", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/addSkills/', {'newSkill': 'math', "name": "alidz"})
        self.assertEqual(rsp.context['Message'], "Failed to add skill", msg="skill should not be added")
        self.assertEqual(list(Skill.objects.filter(owner=self.validUser)).__len__(), 1)

    def test_sameSkill_multiUser(self):
        self.supervisor.post('/', {"name": "lucy", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/addSkills/', {'newSkill': 'math', "name": "lucy"})
        self.assertEqual(rsp.context['Message'], "Success!", msg="skill should be added")
        self.assertEqual(list(Skill.objects.filter(owner=self.validUser2)).__len__(), 1)
        self.assertEqual(rsp.context['mySkills'], list(Skill.objects.filter(owner=self.validUser2)), msg="list should still be empty")