from django.urls import path

from . import views

urlpatterns = [
    path('', views.submit, name='submit'),
    path('jobs/<str:job_id>/', views.jobs, name='job lookup'),
    path('jobs/', views.jobs, name='job submit'),
]

