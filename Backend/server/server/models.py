#models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, primary_key=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=50)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class FCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

class Message(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    recipient_token = models.CharField(max_length=255)
    firebase_response = models.TextField()

