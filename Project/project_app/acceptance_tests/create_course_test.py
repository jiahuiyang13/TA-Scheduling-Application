from django.test import TestCase, Client
from project_app.models import Course, User

class TestCreateCourse(TestCase):
    supervisor = None
    thingList = None
    def setUp(self):
        self.supervisor = Client()
        self.user = User.objects.create(username="alidz", password="star")
        self.course1 = Course.objects.create(name="CS 150", dateTime="2022-02-12 14:30:34").save()
        self.course2 = Course.objects.create(name="CS 250", dateTime="2022-02-12 14:30:34").save()

    def test_addCourse(self):
        self.supervisor.post('/', {"name": "alidz", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/createCourse/', {'courseName': 'CS 351', 'courseTime': "2022-02-12 14:30:34"})
        self.assertEqual(rsp.context['Message'], "course creation successful", msg="list should be updated with new item added")
        self.assertEqual(list(Course.objects.all()).__len__(), 3)

    def test_duplicateCourse(self):
        self.supervisor.post('/', {"name": "alidz", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/createCourse/', {'courseName': 'CS 250', 'courseTime': "2022-02-12 14:30:34"})
        self.assertEqual(rsp.context['Message'], "course already exists", msg="duplicate courses should cause error")
        self.assertEqual(list(Course.objects.all()).__len__(), 2, msg='number of courses should not change from original set up')

    def test_invalidFormat(self):
        self.supervisor.post('/', {"name": "alidz", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/createCourse/', {'courseName': "CS 550", 'courseTime': "5:15"})
        self.assertEqual(rsp.context['Message'], "time must be YYYY-MM-DD HR:MN:SC",
                         msg="should not add course with invalid time")
        self.assertEqual(list(Course.objects.all()).__len__(), 2, msg='courses in db should not change')

    def test_courseList(self):
        self.supervisor.post('/', {"name": "alidz", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/createCourse/')
        self.assertEqual("CS 150", rsp.context['course_list'][0].name, msg="Course list inaccurate/not found")
        self.assertEqual("CS 250", rsp.context['course_list'][1].name, msg="Course list inaccurate/not found")

    def test_courseList_add(self):
        self.supervisor.post('/', {"name": "alidz", "password": "star"}, follow=True)
        rsp = self.supervisor.post('/home/createCourse/', {'courseName': "CS 550", 'courseTime': "2022-02-12 14:30:34"})
        self.assertEqual("CS 150", rsp.context['course_list'][0].name, msg="Course list inaccurate/not found")
        self.assertEqual("CS 250", rsp.context['course_list'][1].name, msg="Course list inaccurate/not found")
        self.assertEqual("CS 550", rsp.context['course_list'][2].name, msg="Course list inaccurate/not found")



