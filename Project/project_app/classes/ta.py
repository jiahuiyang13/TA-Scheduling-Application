from project_app.classes.user import user
from project_app.models import User, Section, Course, Skill

class Ta(user):

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

    def editInfo(self, username, new_phone, new_name, new_email, new_address ):
        pass

    def addSkills(self,skill, ta):
       if(User.objects.filter(username=ta) is None): return False
       print(User.objects.get(username=ta).user_type)
       print("TA")
       if((User.objects.get(username=ta).user_type) != "ta"): return False
       if(len(list((Skill.objects.filter(name=skill, owner=User.objects.get(username=ta)))))>0): return False
       Skill.objects.create(name=skill, owner=User.objects.get(username=ta))
       return True


