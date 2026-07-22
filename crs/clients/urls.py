from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:pk>/', views.view, name='client_view'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('search/', views.search, name='search'),
]