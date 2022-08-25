from django.db.utils import IntegrityError
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart, CartItem
from products.models import Product
from billing.models import BillingProfile, Payment
from billing.serializers import BillingProfileSerializer


class BillingProfileAPIView(ListCreateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = BillingProfileSerializer

  def get_queryset(self):
    self.request.POST.user = self.request.user
    return self.request.user.billingprofile_set.all()

  def create(self, request, *args, **kwargs):
    # Get The Request Data
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email', request.user)
    payment_method = data.get('payment_method', 'visa')
    payment_id = data.get('payment_id', 123789)
    address_line_1 = data.get('address')
    address_line_2 = data.get('address_2')
    city = data.get('city', 'Ho Chi Minh')
    # cart_id = request.session.session_key
    # cart = Cart.objects.get(id=cart_id, used=False)
    user = request.user
    try:
      if request.user and request.user.is_authenticated:
        if Cart.objects.filter(user__email=request.user, used=False).count() == 1:
          cart = Cart.objects.get(user__email=request.user, used=False)
          payment = Payment.objects.create(
            user=request.user,
            payment_method=payment_method,
            payment_id=payment_id,
            amount_paid=cart.total_amount
          )
          # Make The Profile And If Any required field is empty then return 400 error
          profile = self.request.user.billingprofile_set.create(
            user = request.user,
            payment = payment,
            name = first_name + ' ' + last_name,
            email = email,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city
          )
          cart_items = CartItem.objects.filter(cart=cart)
          for item_product in cart_items:
            product = Product.objects.get(id=item_product.product.id, active=True)
            if product is not None:
              product.quantity -= item_product.quantity
              if product.quantity < 0:
                product.quantity = 0
              product.save()

          cart.used = True
          cart.save()
    except IntegrityError as err:
      return Response({"error": "Insufficient Data"}, status=400)
    # If Everything goes smooth then return the profile
    return Response(self.serializer_class(profile).data)

