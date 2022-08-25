
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from billing.models import BillingProfile
from cart.models import Cart
from products.models import Product

from .models import Order
from .serializers import DetailedOrderSerializer


class CheckoutView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kwargs):
    profile_id = request.GET.get("profile_id")

    if profile_id == None:
      return Response({'error': 'Profile Id Not Found'}, status=400)

    profiles = BillingProfile.objects.filter(id=profile_id)

    if not profiles.count() == 1:
      return Response({'error': 'Profile Doesn\'t exist'}, status=400)

    cart_obj, _ = Cart.objects.get_existing_or_new(request)

    if cart_obj.total_cart_products == 0:
      return Response({'error': 'Cart Is Empty'}, status=400)

    order_obj = Order.objects.get_order(profiles.first())

    return Response({
      "order": DetailedOrderSerializer(order_obj, context={'request': request}).data,
      "secret": intent.client_secret
    })

  def post(self, request, *args, **kwargs):
    pass

