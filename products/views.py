from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import authentication, permissions, serializers, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view

from .models import Product, Tag
from .serializers import ProductSerializer
from category.models import Category

User = get_user_model()


@api_view(['GET'])
def getProductsNewest(request, *args, **kwargs):
  products = Product.objects.filter().order_by('-timestamp')[:3]
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getProductsHighView(request, *args, **kwargs):
  products = Product.objects.all().order_by('-views')[:3]
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getProductsBestSeller(request, *args, **kwargs):
  products = Product.objects.all().order_by('-sold')[:3]
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getProductsWithCategory(request, id_category, *args, **kwargs):
  products = Product.objects.filter(category=id_category)
  list_products = list(products)
  serializer = ProductSerializer(list_products, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getProductWithNameCategory(request, name_category, *args, **kwargs):
  category = Category.objects.filter(name=name_category, active=True).first()
  list_products = []
  if category is not None:
    sub_categories = Category.objects.filter(parent=category.id, active=True)
    products = Product.objects.filter(category=category)
    list_products += list(products)
    for cate in sub_categories:
      products = Product.objects.filter(category=cate.id, active=True)
      list_products += list(products)

    serializer = ProductSerializer(list_products, many=True)
    return Response(serializer.data)
  return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getManyProductsDifferWithCategory(request, id_category, *args, **kwargs):
  subs_categories = Category.objects.filter(parent=id_category)
  list_products = []
  products = Product.objects.filter(category=id_category)
  list_products += list(products)
  for cate in subs_categories:
    data_products = Product.objects.filter(category=cate.id)
    list_products += list(data_products)

  serializer = ProductSerializer(list_products, many=True)
  return Response(serializer.data)


class ProductAPIView(APIView):
  def get(self, request):
    products_men = Product.objects.filter(Q(gender=0))[:4]
    products_women = Product.objects.filter(Q(gender=1))[:4]
    products_accessories = Product.objects.filter(category=16)[:4]
    products_kids = Product.objects.filter(category=29)[:4]
    products = list(products_men) + list(products_women) + list(products_accessories) +  list(products_kids)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

  def post(self, request):
    try:
      serializer = ProductSerializer(data=request.data, many=False)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response('create product success!')
    except:
      str_error = ''
      errors = serializer.errors
      for key, values in errors.items():
        str_error += key
        for text in values:
          str_error += ' ' + text
      return Response(str_error.lower())


class ProductViewSet(ModelViewSet):
  serializer_class = ProductSerializer
  permission_classes = [permissions.AllowAny]
  lookup_field = 'id'

  def get_queryset(self):
    products_men = Product.objects.filter(Q(gender=0))[:4]
    products_women = Product.objects.filter(Q(gender=1))[:4]
    products = list(products_men) + list(products_women)
    return products

  def retrieve(self, request, id, *args, **kwargs):
    instance = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(instance, many=False)
    return Response(serializer.data)

  def create(self, request, *args, **kwargs):
    try:
      serializer = ProductSerializer(data=request.data, many=False)
      if serializer.is_valid(raise_exception=True):
        product = serializer.save()
        return Response('product created success!')
    except:
      str_error = ''
      errors = serializer.errors
      for key, values in errors.items():
        str_error += key
        for text in values:
          str_error += ' ' + text
      return Response(str_error.lower())


  def destroy(self, request, id, *args, **kwargs):
    product = Product.objects.get(id=id)
    if product:
      try:
        product.delete()
        return Response('delete product success!')
      except:
        return Response('can not delete product')
    return Response('product not found')

  def update(self, request, id, *args, **kwargs):
    product = Product.objects.get(id=id)
    try:
      if product:
        data_product = request.data
        product.title = data_product.get('title', product.title)
        if request.FILES['image']:
          product.image = request.FILES['image']
        product.description = data_product.get('description', product.description)
        product.active = data_product.get('active', product.active)
        product.featured = data_product.get('featured',product.featured)
        product.original_price = data_product.get('original_price', product.original_price)
        product.price = data_product.get('price', product.price)
        product.tax = data_product.get('tax', product.tax)
        product.save()
        return Response('update product success!')
    except:
      return Response('can not update product!')



class RelatedProductView(APIView):
  permission_classes = [permissions.AllowAny]

  def get(self, request, id, *args, **kwargs):
    product_id = id  # request.data.get("product_id")
    if not product_id:
      return Response({"error": "Product Id Not Found"}, status=400)
    product = get_object_or_404(Product, id=product_id)
    products_serialized = ProductSerializer(
      product.get_related_products(), many=True, context={'request': request})
    return Response(products_serialized.data)

  @classmethod
  def get_extra_actions(cls):
    return []


