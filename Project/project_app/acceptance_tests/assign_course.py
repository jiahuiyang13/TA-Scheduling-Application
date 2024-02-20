from django.test import TestCase, Client
from project_app.models import User, Course

class AssignCourseTest(TestCase):
    def setUp(self):
        self.admin = Client()
        self.ADMIN = User.objects.create(username="admin", password="admin", name="admin",
                                         email="admin@example.com", phone="1234567890",
                                         address="123 Admin lane, Springfield, Illinois ", user_type="admin")
        self.INS = User.objects.create(username="userone", password="1234", name="userone",
                                       email="userone@example.com", phone="1234567890",
                                       address="123 Roadrage lane, Springfield, Illinois ", user_type="instructor")
        self.course1 = Course.objects.create(name="courseone", dateTime="2023-05-15 10:00:00")

    def test_assignCourse(self):
        self.admin.post('/', {"name": "admin", "password": "admin"}, follow=True)
        response = self.admin.post('/home/assignCourse/', {'courseID': 'courseone', 'userToFind': "userone"})
        self.assertEqual(response.context['Message'], "Course assigned successfully", msg="Course Not Assigned")

    def test_assignCourse_InvalidCourse(self):
        self.admin.post('/', {"name": "admin", "password": "admin"}, follow=True)
        response = self.admin.post('/home/assignCourse/', {'courseID': 'nonexistentcourse', 'userToFind': "userone"})
        self.assertEqual(response.context['Message'], "Course not found", msg="Invalid Course Assigned")

    def test_assignCourse_InvalidUser(self):
        self.admin.post('/', {"name": "admin", "password": "admin"}, follow=True)
        response = self.admin.post('/home/assignCourse/', {'courseID': 'courseone', 'userToFind': "nonexistentuser"})
        self.assertEqual(response.context['Message'], "User not found", msg="Invalid User Assigned")

    def test_assignCourse_AlreadyAssigned(self):
        self.admin.post('/', {"name": "admin", "password": "admin"}, follow=True)
        self.admin.post('/home/assignCourse/', {'courseID': 'courseone', 'userToFind': "userone"})
        response = self.admin.post('/home/assignCourse/', {'courseID': 'courseone', 'userToFind': "userone"})
        self.assertEqual(response.context['Message'], "Course already assigned", msg="Course Reassigned")
