from django.conf.urls import url, include
from django.urls import path
from . import views
from django.views.generic import TemplateView
from user import views as users
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^dashboard/$', users.DashboardView, name='dashboard'),
    url(r'^profile/$', login_required(users.ProfileView.as_view()), name='profile'),
    url(r'^uploadphoto/$', login_required(users.ProfileView.as_view()), name='uploadphoto'),
    url(r'^user/all_exams/$', login_required(users.AllExams.as_view()), name='all_exams'),
    url(r'^user/new_exam/$', login_required(users.CreateNewExam.as_view()), name='new_exam'),
    url(r'^user/submit_create_exam/$', login_required(users.SubmitCreateNewExam.as_view()), name='submit_create_exam'),
    url(r'^user/check_result/$', login_required(users.Result_View.as_view()), name='check_result')
]
