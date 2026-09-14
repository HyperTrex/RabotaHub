from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('language/<str:language>/', views.set_language, name='set_language'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('jobs/', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('save/<int:job_id>/', views.save_job, name='save_job'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('dashboard/', views.employer_dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.messages, name='messages'),
    path('messages/compose/', views.compose_message, name='compose_message'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
]
