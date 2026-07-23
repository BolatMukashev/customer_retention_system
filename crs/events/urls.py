from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:pk>/', views.view, name='event_view'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/archive/', views.archive, name='archive'),
]