from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('adapter/', views.adapter, name='demo'),
    path('demo/', views.demo, name='demo'),
    path('auth/', views.u_auth, name='auth'),
    path('support/', views.support, name='support'),
]