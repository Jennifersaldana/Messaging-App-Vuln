from django.urls import path
from  . import views

urlpatterns = [
    path('login_user/', views.login_user, name="login"),
    #path('register_user', views.register_user, name="register_user"),
    path('logout/', views.logout_user, name='logout'),
    path('lockout/', views.lockout, name="lockout"),
    path('join/', views.join, name='join'),
]
