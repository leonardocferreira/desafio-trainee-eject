from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
#from uuid import uuid4

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatório')
        if not password:
            raise ValueError('Senha é obrigatória')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserModel(AbstractBaseUser, PermissionsMixin): 
    #id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Full Name')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    address = models.CharField(max_length=255, verbose_name='Address')
    birth_date = models.DateField(verbose_name='Birth Date')
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number')
    cpf = models.CharField(unique=True, max_length=14, verbose_name='CPF')
    cep = models.CharField(max_length=9, verbose_name='CEP')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        #ordering = ['-updated_at']
    
    def __str__(self):
        return f'{self.name} - {self.email}'