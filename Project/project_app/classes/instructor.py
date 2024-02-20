from project_app.classes.user import user
from project_app.models import User, Section, Course

class Instructor(user):
    def login(self, name, password):
        if not isinstance(name, str): raise TypeError("Username must be a string")
        if not isinstance(password, str): raise TypeError("Password must be a string")
        try:
            myUser = User.objects.get(username=name)
        except User.DoesNotExist:
            return False
        if myUser.password == password:
            return True
        else:
            return False

    def editInfo(self, username, new_phone, new_name, new_email, new_address):
        pass

    def viewMyInfo(self, name, password):
        if isinstance(name, str) == False: raise TypeError("must be string")
        if isinstance(password, str) == False: raise TypeError("must be string")
        myUser = User.objects.filter(username=name)
        myUser = myUser.filter(password=password).first()
        return myUser

    def searchCourse(self,course):
        if isinstance(course, str) == False: raise TypeError("must be string")
        courseList = list(Course.objects.filter(name__exact=course))
        return (len(courseList) == 1)

    def searchUser(self, name):
        pass
    def assignSection(self, course, section, assignee):
        s = list(Section.objects.filter(sectionName__exact=section))
        c = list(Course.objects.filter(name__exact=course))
        u = list(User.objects.filter(username__exact=assignee))

        if len(u) == 0: # if there isn't a user with assignee name raise error
            raise ValueError("Assignee not found")
        else:
            myUser = u[0]

        if len(c) == 0: # if there is no course raise error
            raise ValueError("Course not found")

        if len(s) == 0: # if there is no section raise error
            raise ValueError("Section not found")

        for i in s: #a for loop just in case there are multiple sections with the same ID
            if i.owner == c[0]:
                secToAssign = i
                break
            raise ValueError("Section entered is not a part of the course entered") # section isn't linked to course

        if secToAssign.user_id == myUser: # check if the user is already assigned
            raise ValueError("Assignee is already assigned to this section")

        secToAssign.user_id = myUser
        secToAssign.save()
        return True



