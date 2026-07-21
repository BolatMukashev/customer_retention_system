from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('client-search', views.client_search, name='client_search'),
]