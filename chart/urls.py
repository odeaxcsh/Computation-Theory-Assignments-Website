from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('assignment/<int:assignment_id>/', views.assignment, name='assignment')
]
