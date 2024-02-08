from django.urls import path

from . import views

urlpatterns = [
    path("", views.viewer, name="viewer"),
    path("<int:assignment>/<int:question>/", views.index, name="submission_page"),
]
