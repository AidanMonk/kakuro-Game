from django.urls import path
from . import views

urlpatterns = [
    path('', views.init_board, name="init_board"),
    path('validate/', views.validate_board, name='validate_board'),
    path('hint/', views.get_hint, name='get_hint'),  # New endpoint for hints
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
]