from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import datetime
from cloudinary.models import CloudinaryField,CloudinaryResource
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from cloudinary_storage.storage import VideoMediaCloudinaryStorage,MediaCloudinaryStorage
from cloudinary_storage.validators import validate_video


# Create your models here.  
class UserManager(BaseUserManager):
 
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise
 
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
 
        return self._create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    """
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
 
    objects = UserManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
    
    def generate_token(self,*args):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'email': self.email,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

class Profile(models.Model):
    '''
    profile class to define profile objects
    '''
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=CloudinaryField('picture',blank=True)
    bio=models.CharField(max_length=100,blank=True)
    contacts=models.CharField(max_length=30,blank=True)

    def __str__(self):
        return self.user

class Tag(models.Model):
    '''
    profile class to define tag object
    '''
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name
  
class InterventionRecord(models.Model):
    '''
    profile class to define InterventionRecord objects
    '''
    STATUS=(
        ('Under Investigation','Under Investigation'),
        ('rejected','rejected'),
        ('resolved','resolved')
    )
    title=models.CharField(max_length=50,blank=False)
    description=models.TextField(blank=True, null=True)
    time_of_creation=models.DateTimeField(auto_now_add=True)
    time_last_edit=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20,choices=STATUS, blank=True, null=True ,default="waiting")
    latitude = models.CharField(max_length=200, blank=True,null=True)
    longitude = models.CharField(max_length=200,blank=True,null=True)
    
    image=models.ImageField(upload_to='images/interventionimages/',blank=True,null=True,storage=MediaCloudinaryStorage(),max_length=100000, default="media/images/intervention_default_ozvizh.jpg")
    videos=models.FileField(upload_to='videos/',blank=True,null=True,storage=VideoMediaCloudinaryStorage(),validators=[validate_video])
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-pk"]

class Flag(models.Model):
    '''
    profile class to define FlagRecord objects
    '''
    STATUS=[
        ('Under Investigation','Under Investigation'),
        ('rejected','rejected'),
        ('resolved','resolved')
    ]
    title = models.CharField(max_length=100)
    description=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default='')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default='')
    tags=models.ManyToManyField(Tag)
    image=models.ImageField(upload_to='images/flagimages/',blank=True,storage=MediaCloudinaryStorage())
    videos=models.FileField(upload_to='videos/',blank=True,storage=VideoMediaCloudinaryStorage(),validators=[validate_video])
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Flags"  
        ordering = ["-pk"]
         
    
    
