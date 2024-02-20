from django.test import TestCase
from project_app.models import Course, User
from project_app.classes.admin import Admin
class TestAssignCourse(TestCase):
    def setUp(self):
        self.admin = Admin()
        self.user1 = User.objects.create(username="userone", password="1234", name="User One",
                                         email="userone@example.com", phone="1234567890",
                                         address="123 Roadrage lane, Springfield, Illinois ", user_type="instructor")
        self.user2 = User.objects.create(username="usertwo", password="4321", name="User Two",
                                         email="usertwo@example.com", phone="0987654321",
                                         address="1325 Barrington Rd, Hoffman Estates, IL 60169", user_type="ta")
        self.course1 = Course.objects.create(name="courseone", dateTime="2023-05-15 10:00:00")
        self.course2 = Course.objects.create(name="coursetwo", dateTime="2023-05-20 13:00:00")

    def test_assignCourse_validInput(self):
        self.admin.assignCourse("userone", "courseone")
        assigned_course = Course.objects.get(name="courseone")
        self.assertEqual(assigned_course.user_id, self.user1, msg="User's assigned courses not updated in database")

    def test_assignCourse_invalidUser(self):
        with self.assertRaises(ValueError, msg="assignCourse() failed to raise error for invalid user"):
            self.admin.assignCourse("userthree", "courseone")

    def test_assignCourse_invalidCourse(self):
        with self.assertRaises(ValueError, msg="assignCourse() failed to raise error for invalid course"):
            self.admin.assignCourse("userone", "coursethree")

    def test_assignCourse_userAlreadyAssigned(self):
        self.course1.user_id = self.user1
        self.course1.save()
        with self.assertRaises(ValueError, msg="assignCourse() failed to raise error for user already assigned"):
            self.admin.assignCourse("userone", "courseone")









