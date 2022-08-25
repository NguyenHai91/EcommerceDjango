from django.db import models
from django.db.models.signals import pre_save
from random import randint
from os import path
from Shop.utils import unique_slug_generator

# Create your models here.

def get_filename_ext(filename):
  filepath = path.basename(filename)
  name, ext = path.splitext(filepath)
  return name, ext


def upload_name_path(instance, filename):
  folderName = randint(1, 40000000)
  filenam = randint(1, folderName)
  ext = get_filename_ext(filename)[1]
  return f'products/{filenam}{ext}'

class Category(models.Model):
  parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
  title = models.CharField(max_length=200)
  name = models.CharField(max_length=200)
  slug = models.SlugField(blank=True)
  image = models.ImageField(upload_to=upload_name_path, null=True, blank=True)
  active = models.BooleanField(default=True)
  timestamp = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.title


def category_pre_save_receiver(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)
  if not instance.name:
    instance.name = instance.title

pre_save.connect(category_pre_save_receiver, sender=Category)