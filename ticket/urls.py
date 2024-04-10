from django.urls import path
from . import views


urlpatterns = [
    path('support', views.login_user, name='support'),
]