import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.files.storage import default_storage, FileSystemStorage
from Shop.settings import STATIC_URL

from Shop.utils import unique_slug_generator, upload_name_path


ROLL_ADMIN = 0
ROLL_STAFF = 1
ROLL_CUSTOMER = 2
ROLL = [(ROLL_ADMIN, 'admin'), (ROLL_STAFF, 'staff'), (ROLL_CUSTOMER, 'customer')]

class MyUserManager(BaseUserManager):
  def create_user(self, email, password, roll=None, username=None):
    if email is False:
      raise ValueError('User must have an email')
    if password is False:
      raise ValueError('User must have an password')
    if re.fullmatch('^[a-z0-9.]+@[a-z0-9]+.[a-z]{2,}$', email.lower()) is False:
      raise ValueError('Sorry, Invalid email address')
    if re.fullmatch('^[a-z0-9.@#$%^&*-+~!]{4,}$', password) is False:
      raise ValueError('Sorry, Invalid password')
    if roll is None:
      roll = ROLL_CUSTOMER

    email = self.normalize_email(email)
    user = self.model(email=email, username=username)
    user.roll = roll
    user.set_password(password)
    user.active = True
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password, username=None):
    user = self.create_user(email=email, password=password, roll=ROLL_ADMIN, username=username)
    return user



class MyUser(AbstractBaseUser):
  username = models.CharField(max_length=200, unique=True, null=True, blank=True)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=250)
  roll = models.SmallIntegerField(choices=ROLL, default=ROLL_CUSTOMER)
  active = models.BooleanField(default=True)
  last_login = models.DateTimeField(auto_now=True)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  objects = MyUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email

  @property
  def is_active(self):
    return self.active

  @property
  def is_staff(self):
    if self.roll == ROLL_STAFF or self.roll == ROLL_ADMIN:
      return True

    return False

  @property
  def is_admin(self):
    return self.roll == ROLL_ADMIN

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True


GENDER_MALE = 0
GENDER_FEMALE = 1
GENDER_UNISEX  = 2
GENDER = [
  (GENDER_MALE, 'Male'),
  (GENDER_FEMALE, 'Female'),
  (GENDER_UNISEX, 'Unisex'),
]

class ProfileUserManager(models.Manager):
  def create_profileuser(self, user, first_name, last_name, gender, avatar=None, phone=None, city=None, address=None):
    if not user:
      raise ValueError('Profile user must have an user')
    if not first_name:
      raise ValueError('Profile user must have an first_name')
    if not last_name:
      raise ValueError('Profile user must have an last_name')
    if not gender:
      gender = GENDER_MALE

    profile_user = self.model(
      user=user,
      first_name=first_name,
      last_name=last_name,
      phone=phone,
      avatar=upload_name_path(self, avatar.name, 'user'),
      gender=gender,
      city=city,
      address=address
    )
    file_system_storage = FileSystemStorage()
    file_system_storage.save(profile_user.avatar, avatar)
    profile_user.save(using=self._db)
    return profile_user


class ProfileUser(models.Model):
  user = models.OneToOneField(MyUser, related_name='profile', on_delete=models.CASCADE)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  avatar = models.ImageField(upload_to='static/user/', null=True)
  phone = models.CharField(max_length=200, null=True, blank=True)
  gender = models.SmallIntegerField(choices=GENDER, default=GENDER_MALE)
  city = models.CharField(max_length=250, null=True, blank=True)
  address = models.CharField(max_length=250, null=True, blank=True)

  objects = ProfileUserManager()

  def __str__(self):
    return self.user.email

  @property
  def get_absolute_image_url(self):
    return f'{STATIC_URL}{self.image.url}'


