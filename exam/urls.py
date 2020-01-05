from django.conf.urls import url, include
from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
app_name = 'onlineexam'

urlpatterns = [
    # url(r'^', views.index, name='index')
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.Objective_exam_create_View, name='create_exam'),
    url(r'^submit/$', views.Objective_exam_submit_View, name='submit_question'),
    # url(r'^exam-created/(?P<exam_id>\d+)/$', TemplateView.as_view(), name='submit_success'),
    url(r'^result/$', views.Result_View.as_view(), name='view_result'),
    url(r'^search/$', views.Search_View.as_view(), name='search_exam_page'),
    url(r'^search_ajax/$', views.search_exam_ajax, name='search_exam'),
    url(r'^(?P<exam_id>\d+)/objective/$', views.Objective_exam_View.as_view(), name='Exam'),
    url(r'^sendEmail/$', views.Send_email, name='send_email'),
    url(r'^login/$', views.login_auth, name='login'),
    # url(r'^login/$', "django.contrib.auth.views.login", name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^forget-password/$', views.forget_password, name='forget_password'),
    path('exam/<str:exam_id>', views.Exam_View.as_view(), name='student_exam'),
    path('submit-exam', views.Student_Exam_submit.as_view(), name='student_exam_submit'),
    path('result/<id>', views.Student_Result.as_view(), name='student_result'),
    url(r'^', include('user.urls'))
]