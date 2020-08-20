from django.db import models
import uuid  # for uuid
import datetime  # for date time ops

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from .managers import UserManager


# Create your models here.
class BaseModel(models.Model):
    """A base model to deal with all the asbtracrt level model creations"""
    class Meta:
        abstract = True

    # uuid field
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    # date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_seconds_since_creation(self):
        """
        Find how much time has been elapsed since creation, in seconds.
        This function is timezone agnostic, meaning this will work even if
        you have specified a timezone.
        """
        return (datetime.datetime.utcnow() -
                self.created_at.replace(tzinfo=None)).seconds


# Create a user model
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """A ORM for users interactions"""
    class Meta:
        """A meta object for defining name of the user table"""
        db_table = "user"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    isVerify = models.BooleanField(default=False)
    isNotify = models.BooleanField(default=False)

    #str function to return name instead of object
    def __str__(self):
        """Return full name in representation instead of objects"""
        return self.first_name + " " + self.last_name

    # use User manager to manage create user and super user
    objects = UserManager()

    # define required fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class DeveloperProfile(BaseModel):
    """
    Model for developer profile
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_num = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "developer_profile"


class Education(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    start_date = models.CharField(max_length=5)
    end_date = models.CharField(max_length=5)
    major = models.CharField(max_length=100)

    class Meta:
        db_table = "education"


class Experience(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=255)
    start_date = models.CharField(max_length=5)
    end_date = models.CharField(max_length=5)
    employment_type = models.CharField(max_length=100)
    city_state = models.CharField(max_length=100)

    class Meta:
        db_table = "experience"


class ProfileSkills(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    skills = models.TextField()

    class Meta:
        db_table = "skills_profile"


class UserProject(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    technology = models.CharField(max_length=250)
    about = models.TextField()

    class Meta:
        db_table = "user_projects"


class PriceAvailablity(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3)
    price = models.IntegerField()
    availablity = models.CharField(max_length=25)

    class Meta:
        db_table = "price_availablity"


class Notification(BaseModel):
    """
    ORM model for managing notification
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deviceId = models.CharField(max_length=100)
    deviceType = models.CharField(max_length=100)
    userType = models.IntegerField()
    deviceToken = models.TextField()

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
