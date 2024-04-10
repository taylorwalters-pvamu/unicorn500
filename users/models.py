from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default= False)
    is_engineer = models.BooleanField(default= False)
    email = models.EmailField(unique = True)