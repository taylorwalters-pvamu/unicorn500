from django.urls import path
from . import views


urlpatterns = [
    path('how_it_works', views.demo_vid, name='demo'),
]