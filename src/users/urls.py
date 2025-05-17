"""File defining the different urls served by user application"""
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

# from . import views


app_name = "users"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path("create/", views.CreateUserView.as_view(), name="createUser"),
    path("list/", views.UserListView.as_view(), name="listUser"),
]