# feedback/urls.py
from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.feedback_list, name='list'),
    path('new/', views.feedback_create, name='new'),
    path('new/<int:offer_id>/', views.feedback_create, name='new_for_offer'),
    path('thanks/', views.feedback_thanks, name='thanks'),
    path('<int:pk>/', views.feedback_detail, name='detail'),
]

