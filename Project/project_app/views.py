from django.shortcuts import render, redirect
from django.views import View
from project_app.models import Course, User, Section, Skill
from project_app.classes.admin import Admin
from project_app.classes.ta import Ta



class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        name = request.POST.get('name')
        password = request.POST.get('password')
        if Admin().login(name, password):
            request.session['name'] = name
            request.session['password'] = password
            return redirect('/home/')

        else:
            return render(request, "login.html", {"errorMessage": "Invalid username or password"})


class Home(View):
    def get(self, request):
        name = request.session["name"]
        password = request.session['password']
        userInfo = Admin().viewMyInfo(name, password)
        return render(request, "home.html", {"name": userInfo.name, "username": userInfo.username, "password": userInfo.password, "phone": userInfo.phone, "email": userInfo.email, "address": userInfo.address})

    def post(self, request):
        username = request.POST.get('name')
        password = request.POST.get('password')
        userInfo = Admin().viewMyInfo(username, password)
        return render(request, "home.html", {"name": userInfo.name, "username": userInfo.username, "password": userInfo.password, "phone": userInfo.phone, "email": userInfo.email, "address": userInfo.address})

class AddSection(View):
    def get(self, request):
        section_list = list(Section.objects.all())
        return render(request, "addSection.html", {"section_list": section_list})

    def post(self, request):
        courseID = request.POST.get("courseID")
        sectionID = request.POST.get("sectionID")
        message = ''

        courseObj = Course.objects.filter(name__exact=courseID)
        sectionObj = Section.objects.filter(sectionName__exact=sectionID)
        if len(courseObj) == 0:
            message = "Course ID not found in database"

        else:
            for i in sectionObj:
                if i.owner.__eq__(courseObj[0]):
                    message = "Section with same ID already exists"
                    break

        if message == '':
            try:
                Admin().createSection(courseID, sectionID)
                message = "Section created"
            except Exception as e:
                message = e
        section_list = list(Section.objects.all())
        return render(request, "addSection.html", {"Message": message, "section_list": section_list})

class CreateDeleteAccount(View):
    admin_instance = Admin()
    def get(self, request):
        # Fetch the list of users
        account_list = list(User.objects.filter())

        # Render the template with the list of users
        return render(request, "createDeleteAccount.html", {"accounts": account_list})

    def post(self, request):
        m = request.session["name"]

        if request.POST.get('username') != None and request.POST.get('username') != '':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            self.admin_instance.create_account(username, password, email)
        userToFind = request.POST.get('userToFind')
        if userToFind != None and userToFind != '':
            self.admin_instance.delete_account(userToFind)

        account_list = list(User.objects.filter())

        return render(request, "createDeleteAccount.html", {"accounts": account_list})


class CreateCourse(View):
    courseList=[]
    def get(self,request):
        course_list = list(Course.objects.all())
        return render(request,"createCourse.html",{"course_list": course_list})

    def post(self, request):
        #check supervisor logged in
        name = request.POST.get('courseName')
        time = request.POST.get('courseTime')
        try:
            a = Admin().createCourse(name, time)
        except TypeError:
            a = "Inputs must be text"
        except ValueError:
            a ="Time must be YYYY-MM-DD HR:MN:SC"
        course_list = list(Course.objects.all())
        Message = a
        return render(request, "createCourse.html", {"Message": Message, "course_list": course_list})

        # if course found return course name
        #else return "course not found"

class AccountEdit(View):

    def get(self, request):
        return render(request,"accountEdit.html",{})

    def post(self, request):
        username = request.session['name']
        field_to_change = request.POST.get("user-fields")
        new_value = request.POST.get("newEntry")

        # Retrieve the user from the database
        user = User.objects.get(username=username)

        if field_to_change in ['phone', 'name', 'email', 'address']:
            # Check for unique constraints for name and email
            if field_to_change == 'name' and User.objects.filter(username=new_value).exclude(
                    username=user.username).exists():
                message = 'Username already exists'
            elif field_to_change == 'email' and User.objects.filter(email=new_value).exclude(
                    username=user.username).exists():
                message = 'Email already exists'
            else:
                setattr(user, field_to_change, new_value)
                user.save()
                message = 'Information updated successfully'
        else:
            message = 'Invalid field selected'

        return render(request, "accountEdit.html", {"Message": message})


class AssignSection(View):
    def get(self, request):
        return render(request,"assignSection.html",{})

    def post(self, request):
        pass


class AssignCourse(View):
    def get(self, request):
        user_list = list(User.objects.all())
        course_list = list(Course.objects.all())
        return render(request, "assignCourse.html", {"user_list": user_list, "course_list": course_list})

    def post(self, request):
        courseID = request.POST.get("courseID")
        userToFind = request.POST.get("userToFind")

        message = ''
        try:
            course = Course.objects.get(name=courseID)
            user = User.objects.get(username=userToFind)
            course.user_id = user
            course.save()
            message = 'Course assigned successfully'
        except Course.DoesNotExist:
            message = 'Course not found'
        except User.DoesNotExist:
            message = 'User not found'

        course_list = list(Course.objects.all())
        user_list = list(User.objects.all())
        userSkills = Skill.objects.filter(owner=user)  # Updated this line

        return render(request, "assignCourse.html",
                      {"Message": message, "course_list": course_list, "user_list": user_list,
                       "userSkills": userSkills})


class AddSkills(View):
    def get(self, request):
        ta1 = request.session["name"]
        mySkills = list(Skill.objects.filter(owner=User.objects.get(username=ta1)))
        return render(request, "addSkills.html", {"mySkills": mySkills}) # add a skill list that gets displayed with the user for view skills

    def post(self, request):
        ta1 = request.session["name"]
        #not sure how to access username, is above correct?
        skill = request.POST.get('newSkill')
        Message= "Success!"
        mySkills = list(Skill.objects.filter(owner=User.objects.get(username=ta1)))
        if Ta().addSkills(skill, ta1):
            mySkills = list(Skill.objects.filter(owner=User.objects.get(username=ta1)))
        else:
            Message = "Failed to add skill"

        return render(request, "addSkills.html", {"Message": Message, "mySkills": mySkills})

class ViewSkills(View):
    def get(self, request):
        return render(request, "viewSkills.html", {})

    def post(self, request):
        user = request.POST.get("userToFind")
        message = ''
        try:
            mySkills = list(Skill.objects.filter(owner=User.objects.get(username=user, user_type='ta')))
        except Exception as e:
            message = str(e)
            return render(request, "viewSkills.html", {"userSkills": "", "Message": message})
        return render(request, "viewSkills.html", {"userSkills": mySkills, "Message": message})

class SearchUser(View):
    def get(self, request):
        user_to_find = request.GET.get('userToFind')
        mySkills = list(Skill.objects.filter(owner=User.objects.get(username=user_to_find, user_type='ta')))
        return render(request, "viewSkills.html", {"accounts": mySkills})

    def post(self, request):
        userToFind = request.POST.get('userToFind')
        Message = "User found"

        if Admin().searchUser(userToFind):
            ta_user = User.objects.get(username=userToFind, user_type='ta')
            mySkills = list(Skill.objects.filter(owner=ta_user))
        else:
            Message = "No user found"

        return render(request, "viewSkills.html", {"Message": Message, "mySkills": mySkills})