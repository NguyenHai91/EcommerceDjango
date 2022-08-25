
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from products.models import Product, Size
from wishlist.models import Wishlist, ItemWishlist


@csrf_exempt
def add_wish(request, id_product, *args, **kwargs):
  wishlist, create = Wishlist.objects.get_wishlist_or_create(request)
  product = Product.objects.get(id=id_product)
  wish_items = ItemWishlist.objects.filter(wishlist=wishlist)
  is_existing = False
  for item in wish_items:
    if item.product_id == product.id:
      is_existing = True
      break

  if is_existing:
    data = {
      'message': 'item is existing'
    }
    return JsonResponse(data, status=400)

  ItemWishlist.objects.create(wishlist=wishlist, product=product)
  wish_items = ItemWishlist.objects.filter(wishlist=wishlist)
  num_wish = len(wish_items)
  data = {
    'num_wish': num_wish
  }
  return JsonResponse(data, status=200)


def delete_wish(request, id_item, *args, **kwargs):
  item_wish = ItemWishlist.objects.get(id=id_item)
  if item_wish is not None:
    item_wish.delete()
    wishlist, created = Wishlist.objects.get_wishlist_or_create(request)
    wish_items = ItemWishlist.objects.filter(wishlist=wishlist)
    num_wish = len(wish_items)
    data = {
      'code': 200,
      'status': 'success',
      'num_wish': num_wish,
      'message': 'item had been delete'
    }
    return JsonResponse(data, status=200)

  data = {
    'code': 400,
    'status': 'error',
    'message': 'item not found'
  }
  return JsonResponse(data, status=400)


def wishlist(request):
  wishlist, created = Wishlist.objects.get_wishlist_or_create(request)
  list_wish = ItemWishlist.objects.filter(wishlist=wishlist)

  data = {
    'items_wish': list_wish
  }
  return render(request, 'wish.html', data)

