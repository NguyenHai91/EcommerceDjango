
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from products.models import Product
from cart.models import Cart
from billing.models import BillingProfile, Payment
from order.models import Order

User = get_user_model()

def order(request):
  cart, created = Cart.objects.get_existing_or_new(request)
  if cart.num_item > 0:
    if request.user.is_authenticated:
      user = User.objects.filter(email=request.user).first()
      context = {
        'user': user,
        'cart': cart,
      }
      return render(request, 'checkout.html', context)

    context = {
      'cart': cart,
    }
    return render(request, 'checkout.html', context)
  else:
    return redirect('/cart/')

def checkout(request):
  if request.method == 'POST':
    cart, created = Cart.objects.get_existing_or_new(request)
    if cart.num_item <= 0:
      context = {
        'code': 400,
        'status': 'error',
        'message': 'Checkout failed, no item in cart',
      }
      return JsonResponse(context)

    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    email = request.POST.get('email', None)
    phone = request.POST.get('phone', None)
    city = request.POST.get('city', None)
    address = request.POST.get('address', None)
    user = User.objects.filter(email=email).first()

    if first_name is None:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'First_name is not empty'
      }
      return JsonResponse(data)
    if last_name is None:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'Last_name is not empty'
      }
      return JsonResponse(data)
    if email is None:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'email is not empty'
      }
      return JsonResponse(data)
    if phone is None:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'phone is not empty'
      }
      return JsonResponse(data)
    if city is None:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'City is not empty'
      }
      return JsonResponse(data)
    if address is None:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'Address is not empty'
      }
      return JsonResponse(data)

    payment = Payment.objects.create(
      user=user,
      payment_id='20392837434',
      payment_method='Cash',
      amount_paid=cart.total_amount
    )
    billing_profile = BillingProfile.objects.create(
      user=user,
      first_name=first_name,
      last_name=last_name,
      email=email,
      phone=phone,
      city=city,
      address=address,
      payment=payment
    )

    if billing_profile.id:
      order = Order.objects.create(
        billing_profile=billing_profile,
        cart=cart,
        shipping_fee=30,
      )
      if order.id:
        for item in cart.cart_items.all():
          product = Product.objects.get(id=item.product_id)
          if product.id:
            product.quantity -= item.quantity
            product.sold += item.quantity
            product.save()

        cart.used = True
        cart.save()
        context = {
          'status_code': 200,
          'status': 'success',
          'message': 'Checkout completed success',
        }
        return JsonResponse(context)

  context = {
    'status_code': 400,
    'status': 'error',
    'message': 'Checkout failed, please check and try against',
  }
  return JsonResponse(context, status=400)

def success(request):
    return render(request, 'success.html')