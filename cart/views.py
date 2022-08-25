from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from products.models import Product, Size, Color

from .models import Cart, CartItem
from .serializers import CartSerializer


class CartAPIView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, *args, **kwargs):
    print(request.session.get('cart_id'))
    cart_obj, _ = Cart.objects.get_existing_or_new(request)
    context = {'request': request}
    serializer = CartSerializer(cart_obj, context=context)
    return Response(serializer.data)

  def post(self, request, *args, **kwargs):
    print('increament quantity')
    # Request Data
    product_id = request.data.get("id")
    id_size = request.data.get('id')
    id_color = request.data.get('id')
    quantity = int(request.data.get("quantity", 1))

    # Get Product Obj and Cart Obj
    product_obj = get_object_or_404(Product, pk=product_id)
    size = None
    color = None
    if id_size:
      size = Size.objects.get(id=id_size)
    if id_color:
      color = Color.objects.get(id=id_color)
    cart_obj, _ = Cart.objects.get_existing_or_new(request)

    if quantity <= 0:
      # Delete item in cart
      cart_item_qs = CartItem.objects.filter(cart=cart_obj, product=product_obj, size=size, color=color)
      if cart_item_qs.count != 0:
        cart_item_qs.first().delete()
    else:
      # Add item into cart
      cart_item_obj, created = CartItem.objects.get_or_create(product=product_obj, cart=cart_obj, size=size, color=color)
      if product_obj.quantity > 0:
        cart_item_obj.quantity += quantity
      cart_item_obj.save()

    serializer = CartSerializer(cart_obj, context={'request': request})
    return Response(serializer.data)

  def delete(self, request, *args, **kargs):
    id_item = request.data.get('id_item')
    cart_id = request.session.get('cart_id')
    if request.user.is_authenticated:
      cart = Cart.objects.get(user=request.user, used=False)
      if cart is not None:
        cart_item = CartItem.objects.get(id=id_item, cart=cart)
        if cart_item is not None:
          cart_item.delete()
          serializer = CartSerializer(cart, context={'request': request})
          return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
          {'error_message': "Can't find item in your cart",
            'error_code': 400},
          status=status.HTTP_400_BAD_REQUEST
        )
      return Response(
        {'error_message': "Can't find your cart",
         'error_code': 400},
        status=status.HTTP_400_BAD_REQUEST
      )

    if cart_id is not None:
      cart = Cart.objects.get(id=cart_id, used=False)
      cart_item = CartItem.objects.get(id=id_item, cart=cart)
      if cart_item is not None:
        cart_item.delete()
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    return Response(
      {'error_message': "Can't find your cart",
       'error_code': 400},
      status=status.HTTP_400_BAD_REQUEST
    )

  def put(self, request, *args, **kargs):
    id_item = request.data.get('id_item', None)
    quantity = request.data.get('quantity', 1)
    if request.user.is_authenticated:
      cart = Cart.objects.get(user=request.user, used=False)
      if cart is not None:
        cart_item = CartItem.objects.get(id=id_item, cart=cart)
        product = Product.objects.filter(id=cart_item.product_id).first()
        if cart_item is not None:
          cart_item.quantity += quantity
          if cart_item.quantity >= 1 and product.quantity >= cart_item.quantity:
            cart_item.save()
            serializer = CartSerializer(cart, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

          return Response({'error_message': "Quantity out of stock.", 'error_code': 400}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error_message': "Can't findout your cart item.", 'error_code': 400},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'error_message': "Can't findout your cart.", 'error_code': 400}, status=status.HTTP_400_BAD_REQUEST)

class CheckProductInCart(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, product_id, *args, **kwargs):
    product_obj = get_object_or_404(Product, pk=product_id)
    cart_obj, created = Cart.objects.get_existing_or_new(request)
    return Response(not created and CartItem.objects.filter(cart=cart_obj, product=product_obj).exists())


