from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#from uuid import uuid4
from datetime import timedelta
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        
        if not email:
            raise ValueError('The Email field is required.')
        if not password:
            raise ValueError('The password field is required.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserModel(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'c', 'Customer'
        SHOPKEEPER = 's', 'Shopkeeper'
    #id = models.UUIDField(primary_key=True, default=uuid4, editable=False) 
    name = models.CharField(max_length=255, verbose_name='Full Name')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Address')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Birth Date')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name='CPF')
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name='CEP')
    role = models.CharField(
        max_length=1,
        choices=Role.choices,
        default=Role.CUSTOMER,
        verbose_name='Role',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name',
    ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.email}'