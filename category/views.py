
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view

from .models import Category
from .serializers import CategorySerializer

# Create your views here.

class CategoryViewSet(ModelViewSet):
  serializer_class = CategorySerializer
  permission_classes = [permissions.AllowAny]
  lookup_field = 'id'

  def get_queryset(self):
    return Category.objects.all()



@api_view(['GET',])
def getSubCategories(request, id_category, *args, **kwargs):
  subs = Category.objects.filter(parent=id_category)
  serializer = CategorySerializer(subs, many=True)
  return Response(serializer.data)