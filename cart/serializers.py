from rest_framework import serializers
from rest_framework.fields import Field

from products.serializers import ProductSerializer, SizeSerializer, ColorSerializer
from users.serializers import UserSerializer
from .models import Cart, CartItem



class CartItemSerializer(serializers.ModelSerializer):
  product = ProductSerializer(read_only=True)
  size = SizeSerializer(read_only=True)
  color = ColorSerializer(read_only=True)

  class Meta:
    model = CartItem
    fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
  cart_items = CartItemSerializer(read_only=True, many=True)
  user = UserSerializer(read_only=True)

  class Meta:
    model = Cart
    total_amount = Field(source='total_amount', default=0.0)
    num_item = Field(source='num_item', default=0)
    fields = ['id', 'user', 'cart_items', 'total_amount', 'num_item', 'tax_total']


