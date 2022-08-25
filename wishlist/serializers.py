
from rest_framework import serializers
from rest_framework.fields import Field

from users.serializers import UserSerializer
from wishlist.models import Wishlist, ItemWishlist
from products.serializers import ProductSerializer


class ItemWishlistSerializer(serializers.ModelSerializer):
  product = ProductSerializer(read_only=True)

  class Meta:
    model = ItemWishlist
    fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  wishlist_items = ItemWishlistSerializer(read_only=True, many=True)

  class Meta:
    model = Wishlist
    count_items = Field(source='count_items', default=0)
    fields = ['id', 'user', 'wishlist_items', 'count_items']