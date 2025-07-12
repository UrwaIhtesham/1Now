from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile_number=None, password=None):
        if not email:                               #email is reuqired for registration
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)                 #conerting the domain part to lowercase to normalize
        user = self.model(email=email, mobile_number=mobile_number)
        user.set_password(password)                         #hashes the password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, mobile_number,password=None):
        user = self.create_user(email, mobile_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)              #unique identifier          #the primary login field as username not in the application
    mobile_number = models.CharField(max_length=15, blank=True, null=True)     #optional field
    is_active = models.BooleanField(default=True)       #can login
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
