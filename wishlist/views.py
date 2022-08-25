from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.models import CartItem
from products.models import Product
from wishlist.models import Wishlist, ItemWishlist
from wishlist.serializers import WishlistSerializer

# Create your views here.

class WishlistView(APIView):
  def get(self, request):
    wishlist, _ = Wishlist.objects.get_wishlist_or_create(request)
    context = {'request': request}
    wishlistSerializer = WishlistSerializer(wishlist, context=context)
    return Response(wishlistSerializer.data)

  def post(self, request, *args, **kwargs):
    id = request.data.get('id', None)
    product = Product.objects.get(id=id)
    wishlist, _ = Wishlist.objects.get_wishlist_or_create(request)

    itemProduct = ItemWishlist.objects.filter(wishlist=wishlist, product=product)
    if itemProduct.count() == 0:
      itemProduct = ItemWishlist.objects.create(wishlist=wishlist, product=product)
      itemProduct.save()

    context = {'request': request}
    wishlist_serializer = WishlistSerializer(wishlist, context=context)
    return Response(wishlist_serializer.data)

  def delete(self, request, *args, **kwargs):
    id_item = request.data.get('id', None)
    wishlist, _ = Wishlist.objects.get_wishlist_or_create(request)
    item = ItemWishlist.objects.filter(wishlist=wishlist, id=id_item).first()
    if item is not None:
      item.delete()

    context = {'request': request}
    wishlist_serializer = WishlistSerializer(wishlist, context=context)
    return Response(wishlist_serializer.data)