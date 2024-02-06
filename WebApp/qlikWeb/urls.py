from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('adapter/', views.adapter, name='adapter'),
    path('demo/', views.demo, name='How it works'),
    path('support/', views.support, name='Support Ticket'),
]