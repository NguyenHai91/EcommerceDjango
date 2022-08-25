from rest_framework import serializers
from rest_framework.fields import Field, ListField, SerializerMethodField

from .models import Product, Tag, Size, Color, ImageProduct


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['title', 'slug', 'product']


class SizeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Size
    fields = ['title', 'code_size']


class ColorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Color
    fields = ['title', 'code_color']


class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ImageProduct
    fields = ['image', 'active']


class ProductSerializer(serializers.ModelSerializer):
  tag_list = TagSerializer(many=True, read_only=True)
  image = serializers.ImageField(use_url=True)
  list_images = ImageSerializer(many=True)
  sizes = SizeSerializer(many=True, read_only=True)
  colors = ColorSerializer(many=True, read_only=True)

  class Meta:
    model = Product
    fields = ['id', 'image', 'list_images', 'title', 'slug', 'tax', 'views', 'quantity', 'sold',
              'featured', 'description', 'original_price', 'price', 'tag_list', 'sizes', 'colors']

  def validate(self, data):
    if not data.get('title'):
      raise serializers.ValidationError('title not null')
    else:
      return data


