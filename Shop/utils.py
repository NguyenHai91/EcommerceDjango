import random
import string

from os import path
from random import randint
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_product_id_generator(instance):
    order_code = random_string_generator(8).upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_code=order_code).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_code


def get_filename_ext(filename):
  filepath = path.basename(filename)
  name, ext = path.splitext(filepath)
  return name, ext


def upload_name_path(instance, file, folder='images'):
  folderName = randint(1, 40000000)
  filename = randint(1, folderName)
  ext = get_filename_ext(file)[1]
  return f'{folder}/{filename}{ext}'