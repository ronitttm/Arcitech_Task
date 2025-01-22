from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = None  # Remove this field
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()



class Content(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=60)
    categories = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="contents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
