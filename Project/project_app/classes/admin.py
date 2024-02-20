from project_app.classes.user import user
from project_app.models import User, Section, Course
import datetime

class Admin(user):

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

    def searchUser(self, username):
        if not isinstance(username, str):
            raise TypeError("username must be a string")
        skillList = User.objects.filter(username=username, user_type='ta')
        return skillList
    #should return true if course in datbase, false otherwise
    def createCourse(self, name, time):
        if isinstance(name, str) == False: raise TypeError("must be string")
        if isinstance(time, str) == False: raise TypeError("must be string")
        if datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") == False: raise ValueError("must be string in datetime format")
        if self.searchCourse(name):
            return "Course already exists"

        Course.objects.create(name=name, dateTime=time)
        return "Course creation successful"
    # return course already exists if found
    # else success message and return true


    def create_account(self, username, password, email):
        if not isinstance(username, str) or not isinstance(password, str) or not isinstance(email, str):
            raise TypeError("Invalid argument type")

        # account = User.objects.create(username=username, password=password, email=email)

        # if User.objects.filter(username=username).exists():
        #     return False
        if User.objects.filter(username=username).exists():
            return False
        else:
            account = User.objects.create(username=username, password=password, email=email)
            return True

    def delete_account(self, username):
        if not isinstance(username, str):
            raise TypeError("Invalid argument type")

        try:
            account = User.objects.get(username=username)
            account.delete()
            return True
        except User.DoesNotExist:
            return False

    def createSection(self, courseID, sectionID):
        if not isinstance(courseID, str) or not isinstance(sectionID, str):
            raise TypeError("Invalid argument type")
        if self.searchCourse(courseID):
            secCourse = list(Course.objects.filter(name__exact=courseID))[0]
        else:
            raise ValueError("Course not found in database")

        if len(list(Section.objects.filter(sectionName=sectionID))) != 0:
            raise ValueError("Duplicate section found in database")

        Section.objects.create(sectionName=sectionID, owner=secCourse)
        return True

    def viewSkills(self, ta):
        pass

    def editInfo(self, username, new_phone, new_name, new_email, new_address):
        if not isinstance(username, str) or not isinstance(new_phone, str) or not isinstance(new_name, str) or not isinstance(new_email, str) or not isinstance(new_address, str):
            raise TypeError("Invalid argument type")

        try:
            user_to_update = User.objects.get(username=username)

            # Check if new name and email are unique
            if User.objects.filter(username=new_name).exclude(username=username).exists():
                raise ValueError("Username already exists")
            if User.objects.filter(email=new_email).exclude(username=username).exists():
                raise ValueError("Email already exists")

            user_to_update.phone = new_phone
            user_to_update.username = new_name
            user_to_update.email = new_email
            user_to_update.address = new_address
            user_to_update.save()
            return True

        except User.DoesNotExist:
            raise ValueError("User not found in database")


    def assignCourse(self, assignee_username, course_name):
        # Validate input types
        if not isinstance(assignee_username, str):
            raise TypeError("assignee_username must be a string")
        if not isinstance(course_name, str):
            raise TypeError("course_name must be a string")

        # Get the user and course objects from the database
        try:
            user = User.objects.get(username=assignee_username)
        except User.DoesNotExist:
            raise ValueError(f"User '{assignee_username}' not found in database")

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            raise ValueError(f"Course '{course_name}' not found in database")

        # Check if the user is already assigned to the course
        if course.user_id == user:
            raise ValueError(f"User '{assignee_username}' is already assigned to course '{course_name}'")

        # Add the course to the user's assigned courses
        course.user_id = user
        course.save()

        # Return success message
        return f"Course '{course_name}' assigned to user '{assignee_username}'"

