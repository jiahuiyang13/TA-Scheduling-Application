from django.test import TestCase
from project_app.models import Course, User, Section
from project_app.classes.admin import Admin

class TestCreateSection(TestCase):
    def setUp(self):
        self.admin = Admin()
        self.course1 = Course.objects.create(name="361", dateTime="2023-04-18 10:32:34.184712")
        self.section1 = Section.objects.create(sectionName="891", owner=self.course1)
        self.course2 = Course.objects.create(name="337", dateTime="2023-04-18 10:32:34.184712")

    def test_SectionExistsInDatabase(self):
        sections = list(Section.objects.filter(sectionName__exact="891"))
        self.assertEqual(sections, [self.section1], msg="Section not found in database")

    def test_createSectionBasic(self):
        self.assertEqual(self.admin.createSection("337", "101"), True, msg="createSection() error: Section creation failed")

    def test_duplicateSection(self):
        with self.assertRaises(ValueError, msg="Duplicate section, must raise error"):
            self.admin.createSection("891", "361")

    def test_invalidSectionName(self):
        with self.assertRaises(TypeError, msg="Invalid name, must raise error"):
            self.admin.createSection(12345, "361")

    def test_invalidCourse(self):
        with self.assertRaises(TypeError, msg="Invalid course name, must raise error"):
            self.admin.createSection("101", 12345)

    def test_courseNotPresent(self):
        with self.assertRaises(ValueError, msg="Invalid course (not in database), must raise error"):
            self.admin.createSection("101", "000")