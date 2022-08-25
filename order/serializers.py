from rest_framework import serializers
from rest_framework.fields import IntegerField

from billing.serializers import BillingProfileSerializer
from cart.serializers import CartSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

  class Meta:
    model = Order
    fields = [
      'order_code', 'status', 'timestamp',
      'shipping_fee', 'amount', 'tax', 'total_amount'
    ]


class DetailedOrderSerializer(serializers.ModelSerializer):
  billing_profile = BillingProfileSerializer()
  cart = CartSerializer()
  order = OrderSerializer()

  class Meta:
    model = Order
    fields = [
      'billing_profile', 'order_code', 'cart', 'status',
      'timestamp', 'shipping_fee', 'amount',
      'tax', 'total_amount',
    ]
    # total_in_paise = IntegerField(source='total_in_paise')
