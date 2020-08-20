"""bluerang_remotehiring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from api import views

urlpatterns = [
    path('users', views.UserList.as_view()),
    path('user/<pk>', views.UserDetails.as_view()),
    path('developerprofile/create', views.DeveloperProfileList.as_view()),
    path('developerprofile/<pk>', views.DeveloperProfileDetails.as_view()),
    path("education/create", views.EducationCreate.as_view()),
    path("educations/<userid>", views.UserEductionList.as_view()),
    path("education/<pk>", views.EducationDetails.as_view()),
    path("experience/create", views.ExperienceCreate.as_view()),
    path("experiences/<userid>", views.UserExperienceList.as_view()),
    path("experience/<pk>", views.ExperienceDetail.as_view()),
    path("profileskill/create", views.ProfileSkillsCreate.as_view()),
    path("profileskills/<userid>", views.UserProfileSkillsList.as_view()),
    path("profileskill/<pk>", views.ProfileSkillsDetail.as_view()),
    path("userproject/create", views.UserProjectCreate.as_view()),
    path("userprojects/<userid>", views.UserProjectList.as_view()),
    path("userproject/<pk>", views.UserProjectDetail.as_view()),
    path("priceavailablity/create", views.PriceAvailablityCreate.as_view()),
    path("priceavailablities/<userid>",
         views.UserPriceAvailablityList.as_view()),
    path("priceavailablity/<pk>", views.PriceAvailablityDetail.as_view()),
    path("login", views.AuthorizeUser.as_view()),
    path("homefeed/<?search_term>", views.CustomerFeed.as_view())
]
