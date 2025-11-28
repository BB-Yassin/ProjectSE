from django.urls import path
from . import views
from client import views as client_views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('packages/', views.packages, name='packages'),
    path('login_signup/', client_views.addUser, name='add_user'),
    
]
