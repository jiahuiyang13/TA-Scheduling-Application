from django.test import TestCase, Client
from project_app.models import Course, User

class TestHome(TestCase):
    supervisor = None
    def setUp(self):
        self.supervisor = Client()
        self.user = User.objects.create(username="JDog", password="HipH0popotimu$", name="Jemaine Clement", email="fotconch@gmail.com", phone="(212) 123-2000", address="2125 Cardrona Valley Road, Cardrona 9382, NZ")

    def test_viewMyInfo(self):
        self.supervisor.post('/', {"name": "JDog", "password": "HipH0popotimu$"}, follow=True)
        rsp = self.supervisor.post('/home', {"name": "JDog", "password": "HipH0popotimu$"}, follow=True)
        self.assertEqual(rsp.context['username'], "JDog", msg="Returned user has the wrong username")
        self.assertEqual(rsp.context['password'], "HipH0popotimu$", msg="Returned user has the wrong password")
        self.assertEqual(rsp.context['name'], "Jemaine Clement", msg="Returned user has the wrong name")
        self.assertEqual(rsp.context['email'], "fotconch@gmail.com", msg="Returned user has the wrong email")
        self.assertEqual(rsp.context['phone'], "(212) 123-2000", msg="Returned user has the wrong phone")
        self.assertEqual(rsp.context['address'], "2125 Cardrona Valley Road, Cardrona 9382, NZ", msg="Returned user has the wrong address")