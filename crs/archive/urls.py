from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.index, name='index'),
    path('client/<int:pk>/unarchive/', views.unarchive_client, name='unarchive_client'),
    path('order/<int:pk>/unarchive/', views.unarchive_order, name='unarchive_order'),
    path('event/<int:pk>/unarchive/', views.unarchive_event, name='unarchive_event'),
]