from django.test import TestCase
from project_app.models import Course, User, Section
from project_app.classes.instructor import Instructor
from project_app.classes.admin import Admin
class TestAssignSection(TestCase):
    def setUp(self):
        self.instructor= Instructor()
        self.INS = User.objects.create(username="userone", password="1234", name="userone",
                                         email="userone@example.com", phone="1234567890",
                                         address="123 Roadrage lane, Springfield, Illinois ", user_type="instructor")
        self.TA = User.objects.create(username="usertwo", password="4321", name="usertwo",
                                         email="usertwo@example.com", phone="0987654321",
                                         address="1325 Barrington Rd, Hoffman Estates, IL 60169", user_type="ta")
        self.course1 = Course.objects.create(name="courseone", dateTime="2023-05-15 10:00:00")
        self.section1 = Section.objects.create(sectionName="891", owner=self.course1, user_id=self.INS)

    def test_assignSection_validInput(self):
        self.instructor.assignSection("courseone", "891", "usertwo")
        assigned_section = Section.objects.get(sectionName__exact="891")
        self.assertEqual(assigned_section.user_id, self.TA, msg="Section not displaying assigned TA")

    def test_assignSection_invalidUser(self):
        with self.assertRaises(ValueError, msg="assignSection() failed to raise error for invalid user"):
            self.instructor.assignSection("courseone", "891", "userthree")

    def test_assignSection_invalidCourse(self):
        with self.assertRaises(ValueError, msg="assignSection() failed to raise error for invalid course"):
            self.instructor.assignSection("coursefive", "891", "usertwo")

    def test_assignSection_invalidSection(self):
        with self.assertRaises(ValueError, msg="assignSection() failed to raise error for invalid section"):
            self.instructor.assignSection("courseone", "111", "usertwo")

    def test_assignSection_userAlreadyAssigned(self):
        self.section1.user_id = self.TA
        self.section1.save()
        with self.assertRaises(ValueError, msg="assignSection() failed to raise error for user already assigned"):
            self.instructor.assignSection("courseone", "891", "usertwo")









