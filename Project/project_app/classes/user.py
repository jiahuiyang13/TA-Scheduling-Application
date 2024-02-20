from project_app.models import User, Section, Course
from abc import ABC, abstractmethod

class user(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def login(self, name, password):
        pass

    @abstractmethod
    def viewMyInfo(self, name, password):
        pass

    @abstractmethod
    def searchCourse(self,course):
        pass

    @abstractmethod
    def searchUser(self, name):
        pass

    @abstractmethod
    def editInfo(self, username, new_phone, new_name, new_email, new_address ):
        pass