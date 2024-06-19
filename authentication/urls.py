# urls.py 
from django.urls import path 
from . import views 
 
urlpatterns = [ 
    path('', views.home, name='home'), 
    path('dashboard/', views.dashboard_view, name='dashboard'),  
    path('assessments/', views.assessments_view, name='assessments'), 
    path('assessments/timed-quiz/', views.timed_quiz_view, name='timed_quiz'), 
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'), 
    path('assessments/surveys/', views.surveys_view, name='surveys'), 
    path('assessments/coding-syntax-identification/', views.coding_syntax_identification_view, name='coding_syntax_identification'), 
    path('login/', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='signup'), 
    path('logout/', views.logout_view, name='logout'), 
    path('refresh-captcha/', views.refresh_captcha, name='refresh_captcha'),
]