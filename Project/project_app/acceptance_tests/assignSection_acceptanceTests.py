from django.test import TestCase, Client
from project_app.models import Course, Section, User
from project_app.classes.instructor import Instructor


class TestAssignSection(TestCase):
    def setUp(self):
        self.instructor = Client()
        self.INS = User.objects.create(username="userone", password="1234", name="userone",
                                       email="userone@example.com", phone="1234567890",
                                       address="123 Roadrage lane, Springfield, Illinois ", user_type="instructor")
        self.TA = User.objects.create(username="usertwo", password="4321", name="usertwo",
                                      email="usertwo@example.com", phone="0987654321",
                                      address="1325 Barrington Rd, Hoffman Estates, IL 60169", user_type="ta")
        self.course1 = Course.objects.create(name="courseone", dateTime="2023-05-15 10:00:00")
        self.section1 = Section.objects.create(sectionName="891", owner=self.course1, user_id=self.INS)

    def test_assignSection(self):
        self.instructor.post('/', {"name": "userone", "password": "1234"}, follow=True)
        response = self.instructor.post('/home/assignSection/', {'courseID': 'courseone', 'sectionID': "891", 'assigneeID': "usertwo"})
        self.assertEqual(response.context['Message'], "Section assign successful!", msg="Basic Section Not Created")


    def test_assignSection_InvalidCourse(self):
        self.instructor.post('/', {"name": "userone", "password": "1234"}, follow=True)
        response = self.instructor.post('/home/assignSection/', {'courseID': 'WrongCourse', 'sectionID': "891", 'assigneeID': "usertwo"})
        self.assertEqual(response.context['Message'], "Course not found", msg="Incorrect Course Not Caught")

    def test_assignSection_InvalidSection(self):
        self.instructor.post('/', {"name": "userone", "password": "1234"}, follow=True)
        response = self.instructor.post('/home/assignSection/', {'courseID': 'courseone', 'sectionID': "WrongSection", 'assigneeID': "usertwo"})
        self.assertEqual(response.context['Message'], "Section not found", msg="Incorrect Section Not Caught")

    def test_assignSection_InvalidAssignee(self):
        self.instructor.post('/', {"name": "userone", "password": "1234"}, follow=True)
        response = self.instructor.post('/home/assignSection/', {'courseID': 'courseone', 'sectionID': "891", 'assigneeID': "WrongAssignee"})
        self.assertEqual(response.context['Message'], "Assignee not found", msg="Incorrect Assignee Not Caught")

    def test_assignSection_AlreadyAssigned(self):
        self.instructor.post('/', {"name": "userone", "password": "1234"}, follow=True)
        self.instructor.post('/home/assignSection/', {'courseID': 'courseone', 'sectionID': "891", 'assigneeID': "usertwo"})
        response = self.instructor.post('/home/assignSection/', {'courseID': 'courseone', 'sectionID': "891", 'assigneeID': "usertwo"})
        self.assertEqual(response.context['Message'], "Assignee is already assigned to this section", msg="Shouldn't be able to assign someone to the same section twice")

    def test_assignSection_SectionNotInCourse(self):
        course2 = Course.objects.create(name="coursetwo", dateTime="2023-05-15 10:00:00")
        section2 = Section.objects.create(sectionName="222", owner=course2, user_id=self.INS)
        self.instructor.post('/', {"name": "userone", "password": "1234"}, follow=True)
        response = self.instructor.post('/home/assignSection/', {'courseID': 'courseone', 'sectionID': "222", 'assigneeID': "usertwo"})
        self.assertEqual(response.context['Message'], "Section entered is not a part of the course entered", msg="Error must be raised if section doesn't match course")