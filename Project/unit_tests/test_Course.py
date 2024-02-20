from django.test import TestCase
from project_app.models import Course, User
from project_app.classes.admin import Admin

# Create your tests here.

class TestHomepage(TestCase):
    def setUp(self):
        self.admin1 = Admin()
        self.user1 = User.objects.create(username="lameGuy000", password="Password1:)", name="Richard Smalls", email="lameguy@uwm.edu", phone="123-4567", address="1614 E North Ave. Milwaukee WI 53211")
        self.user2 = User.objects.create(username="c00lguy100", password="P@ssw0rd", name="Hugh Mungus", email="coolguy@uwm.edu", phone="867-5309", address="2100 E. Kenwood Blvd. Milwaukee WI 53211")

    def test_userInfoCorrect(self):
        myInfo = self.admin1.viewMyInfo("c00lguy100", "P@ssw0rd")
        self.assertEqual(myInfo.username, "c00lguy100", "user's username is not correct")
        self.assertEqual(myInfo.password, "P@ssw0rd", "user's password is not correct")
        self.assertEqual(myInfo.name, "Hugh Mungus", "user's name is not correct")
        self.assertEqual(myInfo.email, "coolguy@uwm.edu", "user's email is not correct")
        self.assertEqual(myInfo.address, "2100 E. Kenwood Blvd. Milwaukee WI 53211", "user's address is not correct")

    def test_invalidUsername(self):
        with self.assertRaises(TypeError, msg="should raise exception since username is not string"):
            self.admin1.viewMyInfo(1, "P@ssw0rd")

    def test_invalidPassword(self):
        with self.assertRaises(TypeError, msg="should raise exception since password is not string"):
            self.admin1.viewMyInfo("c00lguy100", 12)

class TestCreateCourse(TestCase):
    def setUp(self):
        self.admin1 = Admin()
        self.course1 = Course.objects.create(name="Intro CS", dateTime="2022-02-12 14:30:34")
        self.course2 = Course.objects.create(name="CS 2", dateTime="2022-02-12 14:30:34")


    def test_CourseInDb(self):
        course_list = list(Course.objects.filter(name__exact="CS 2"))
        self.assertEqual(course_list, [self.course2], msg='course should be in database')

    def test_courseExists(self):
        self.assertEqual(self.admin1.createCourse("Intro CS", "2022-02-12 14:30:34"), "Course already exists", msg='should have returned course already exists msg')

    def test_newCourse(self):
        self.assertEqual(self.admin1.createCourse("Data Structures", "2022-02-12 14:30:34"), "Course creation successful", msg='should have added course and returned success msg')

    def test_invalidCourse(self):
        with self.assertRaises(TypeError, msg="should raise exception for invalid name type"):
            self.admin1.createCourse(38432489238, 1430)

    def test_invalidTimeFormat(self):
        with self.assertRaises(ValueError, msg="should raise exception for invalid time type"):
            self.admin1.createCourse("Intro History", "cats")

    def test_invalidTimeType(self):
        with self.assertRaises(TypeError, msg="should raise exception for invalid time type"):
            self.admin1.createCourse("Intro History", 1413)

class TestSearchCourse(TestCase):
    def setUp(self):
        self.admin1 = Admin()
        self.course1 = Course.objects.create(name="Intro CS", dateTime="2022-02-12 14:30:34.339504")
        self.course2 = Course.objects.create(name="CS 2", dateTime="2022-02-12 14:30:34.339504")

    def test_courseExists(self):
        self.assertTrue(self.admin1.searchCourse("Intro CS"), msg='should have returned true since course is in db')

    def test_noCourse(self):
        self.assertFalse(self.admin1.searchCourse("Geography"), msg='should have returned false since course is not in db')

    def test_invalidInput(self):
        with self.assertRaises(TypeError, msg="should raise exception for invalid search type"):
            self.admin1.searchCourse(143)


