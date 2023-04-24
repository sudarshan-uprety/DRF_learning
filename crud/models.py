from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from .manager import Usermanager

# Create your models here.

class User(AbstractUser):
    username=None
    name=models.CharField( max_length=50)
    email=models.EmailField( max_length=254,unique=True)
    phone=models.IntegerField()
    address=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=Usermanager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name','phone','address','password']

    



class Post(models.Model):
    email=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    content=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

