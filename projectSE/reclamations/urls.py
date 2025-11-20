# reclamations/urls.py
from django.urls import path
from . import views

app_name = 'reclamations'

urlpatterns = [
    path('', views.reclamation_list, name='list'),
    path('new/', views.reclamation_create, name='new'),
    path('<int:pk>/', views.reclamation_detail, name='detail'),
    path('<int:pk>/comment/', views.reclamation_add_comment, name='add_comment'),
]
