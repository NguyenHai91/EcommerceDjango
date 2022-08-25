
from rest_framework import serializers

from .models import Category


class SubcategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'title', 'parent', 'image']


class CategorySerializer(serializers.ModelSerializer):
  subcategories = SubcategorySerializer(many=True, read_only=True)

  class Meta:
    model = Category
    fields = ['id', 'title', 'slug', 'parent', 'image', 'subcategories']
