# anketa/urls.py

from django.urls import path
from . import views

app_name = 'anketa'

urlpatterns = [
    path('<uuid:token>/', views.anketa, name='anketa'),
]