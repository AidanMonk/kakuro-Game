from django.urls import path
from . import views

urlpatterns = [
    path('', views.init_board, name="init_board"),
    path('validate/', views.validate_board, name='validate_board'),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
]