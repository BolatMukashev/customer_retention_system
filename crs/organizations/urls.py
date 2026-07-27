from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    path('', views.index, name='index'),
    path('apply/', views.apply, name='apply'),
    path('apply/success/', views.apply_success, name='apply_success'),
]