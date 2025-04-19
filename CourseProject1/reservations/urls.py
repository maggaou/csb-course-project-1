from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginView, name="login"),
    path("add/", views.createReservation, name="add"),
    path("view/", views.viewReservation, name="view"),
    path("edit/", views.editReservation, name="edit"),
    path("register/", views.createUser, name="register")
]