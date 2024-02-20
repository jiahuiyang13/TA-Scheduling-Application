from django.test import TestCase, Client
from project_app.models import Course, User, Skill

class ViewSkillsTest(TestCase):
    def setUp(self):
        self.Admin = Client()
        # Create a TA user in the system
        self.ta_user = User.objects.create(username='joe', user_type='ta')
        # Create some skills for the TA user
        Skill.objects.create(name='math', owner=self.ta_user)
        Skill.objects.create(name='science', owner=self.ta_user)
    def test_ta_user_in_system(self):
        self.Admin.post('/', {"name": "admin", "password": "admin"}, follow=True)
        response = self.Admin.post('/home/viewSkills/', {'userToFind': 'joe'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(Skill.objects.filter(owner=User.objects.get(username='joe', user_type='ta'))).__len__(), 2,
                         msg='not correct count of TAs skills')

    def test_ta_user_not_in_system(self):
        self.Admin.post('/', {"name": "admin", "password": "admin"}, follow=True)
        response = self.Admin.post('/home/viewSkills/', {'userToFind': 'nobody'})
        self.assertEqual(response.context['Message'], "User matching query does not exist.", msg="Non existent TA Not Caught")
