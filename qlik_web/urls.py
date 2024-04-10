from django.urls import path, include
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('adapter/', views.adapter, name='adapter'),
    path('demo/', views.demo, name='demo'),
    path('support/', views.submit_ticket, name='support'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
]