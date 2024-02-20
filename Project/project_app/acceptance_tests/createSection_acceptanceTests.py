from django.test import TestCase, Client
from project_app.models import Course, Section, User

class TestCreateSection(TestCase):
    def setUp(self):
        self.Supervisor = Client()
        self.User = User.objects.create(username="admin", password="admin")
        self.course1 = Course.objects.create(name="361", dateTime="2022-02-12 14:30:34").save()
        self.section1 = Section.objects.create(sectionName="891", owner=self.course1)

    def test_addSection(self):
        self.Supervisor.post('/', {"name": "admin", "password": "admin"}, follow=True)
        response = self.Supervisor.post('/home/addSection/', {'courseID': '361', 'sectionID': "101"})
        self.assertEqual(response.context['Message'], "Section created", msg="Section not created from post")

    def test_duplicate(self):
        self.Supervisor.post('/', {"name": "admin", "password": "admin"}, follow=True)
        response = self.Supervisor.post('/home/addSection/', {'courseID': '361', 'sectionID': "891"})
        self.assertEqual(response.context['Message'], "Section with same ID already exists", msg="Duplicate section should not be made")

    def test_courseDNE(self):
        self.Supervisor.post('/', {"name": "admin", "password": "admin"}, follow=True)
        response = self.Supervisor.post('/home/addSection/', {'courseID': '1234', 'sectionID': "101"})
        self.assertEqual(response.context['Message'], "Course ID not found in database", msg="Section should not be made for a course that DNE")

    def test_sectionList(self):
        self.Supervisor.post('/', {"name": "admin", "password": "admin"}, follow=True)
        rsp = self.Supervisor.post('/home/addSection/')
        self.assertEqual("891", rsp.context['section_list'][0].sectionName, msg="Section list inaccurate/not found")

    def test_sectionList_add(self):
        self.Supervisor.post('/', {"name": "admin", "password": "admin"}, follow=True)
        rsp = self.Supervisor.post('/home/addSection/', {'courseID': '361', 'sectionID': "101"})
        self.assertEqual("891", rsp.context['section_list'][0].sectionName, msg="Section list inaccurate/not found")
        self.assertEqual("101", rsp.context['section_list'][1].sectionName, msg="Section list inaccurate/not found")
