"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project_app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('home/', Home.as_view()),
    path('home/createCourse/', CreateCourse.as_view()),
    path('home/addSection/', AddSection.as_view()),
    path('home/createDeleteAccount/', CreateDeleteAccount.as_view()),
    path('home/accountEdit/', AccountEdit.as_view()),
    path('home/assignSection/', AssignSection.as_view()),
    path('home/assignCourse/', AssignCourse.as_view()),
    path('home/addSkills/', AddSkills.as_view()),
    path('home/viewSkills/', ViewSkills.as_view())
]
