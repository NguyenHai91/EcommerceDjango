
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from products.models import Product, Size, Color
from cart.models import Cart, CartItem



def delete_item(request, id):
  item = CartItem.objects.get(id=id)
  if item is not None:
    item.delete()

  cart, created = Cart.objects.get_existing_or_new(request)
  cart_items = []
  if created is False:
    cart_items = CartItem.objects.filter(cart=cart)

  data = {
    'num_cart': cart.num_item,
  }
  return JsonResponse(data)

def cart(request):
  cart, created = Cart.objects.get_existing_or_new(request)
  context = {
    'cart': cart
  }
  return render(request, 'cart.html', context)


def check_existing_item(request, id_product, id_size=None, id_color=None):
  cart, created = Cart.objects.get_existing_or_new(request)
  items_cart = cart.cart_items.all()
  product = Product.objects.get(id=id_product)
  size = None
  color = None

  if id_size:
    size = Size.objects.get(id=id_size)
  if id_color:
    color = Color.objects.get(id=id_color)

  if created or cart.num_item <= 0:
    return False, None

  if not product.id:
    return False, None

  if size and color:
    for item in items_cart:
      if item.product_id == product.id and item.size == size and item.color == color:
        return True, item.id

  if size:
    for item  in items_cart:
      if item.product_id == product.id and item.size == size:
        return True, item.id

  if color:
    for item in items_cart:
      if item.product_id == product.id and item.color == color:
        return True, item.id

  if not size and not color:
    for item in items_cart:
      if item.product_id == product.id:
        return True, item.id

  return False, None



def add_cart(request, id, quantity, *args, **kwargs):
  id_size = request.GET.get('size')

  if id_size:
    id_size = int(id_size)

  id_color = request.GET.get('color')

  if id_color:
    id_color = int(id_color)

  product = Product.objects.get(id=id)
  cart, created = Cart.objects.get_existing_or_new(request)
  is_product_existing, id_item_existing = check_existing_item(request, id, id_size, id_color)

  if is_product_existing:
    item_existing = CartItem.objects.get(id=id_item_existing)
    item_existing.quantity += quantity
    item_existing.save()
  else:
    cart_item = None
    if id_size and id_color:
      size = Size.objects.get(id=id_size)
      color = Color.objects.get(id=id_color)
      cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=product.price, size=size, color=color)
    elif id_size:
      size = Size.objects.get(id=id_size)
      cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=product.price, size=size)
    elif id_color:
      color = Color.objects.get(id=id_color)
      cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=product.price, color=color)
    else:
      cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=product.price)

    cart_item.quantity = quantity
    cart_item.save()

  data = {
    'status': 200,
    'message': 'success',
    'num_cart': cart.num_item
  }
  return JsonResponse(data, status=200)


@csrf_exempt
def update_cart(request, *args, **kwargs):
  id_item = request.POST.get('idItem')
  id_item = int(id_item)

  quantity = request.POST.get('quantity')
  quantity = int(quantity)
  item_cart = CartItem.objects.get(id=id_item)
  if item_cart is not None:
    if quantity <= item_cart.product.quantity:
      item_cart.quantity = quantity
      item_cart.save()
      cart = Cart.objects.get(id=item_cart.cart_id)
      data = {
        'status_code': 200,
        'num_cart': cart.num_item,
      }
      return JsonResponse(data)

    data = {
      'status_code': 400,
      'message': 'Sorry, product is not enough quantity'
    }
    return JsonResponse(data)

  data = {
    'status_code': 400,
    'message': 'Sorry, product is not found'
  }
  return JsonResponse(data)