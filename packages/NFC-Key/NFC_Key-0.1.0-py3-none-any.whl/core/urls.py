from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.home, name='home'),
    # path('register', views.register, name='register'),
    path('login', LoginView, name='login'),
    path('logout', LogoutView, name='logout'),
    path('description', views.description, name='description'),
    path('control_panel', views.control_panel, name='control_panel'),
]
