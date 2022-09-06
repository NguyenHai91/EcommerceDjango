
from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings

from category.models import Category
from products.models import Product
from wishlist.models import Wishlist, ItemWishlist



def get_products_many_category(page=1, num_item=settings.NUM_ITEM):
  products = []
  end = int(page) * num_item
  start = end - num_item
  men_category = Category.objects.filter(title__iexact='men').first()
  if men_category is not None:
    men_products = []
    men_products += Product.objects.filter(category=men_category, quantity__gt=0)[start:end].values()
    sub_men_categories = Category.objects.filter(parent=men_category)
    if sub_men_categories.count() > 0:
      for item in sub_men_categories:
        products_in_category = Product.objects.filter(category=item, quantity__gt=0)[start:end].values()
        if products_in_category:
          men_products += products_in_category

    products += men_products

  women_category = Category.objects.filter(title__iexact='women').first()
  if women_category is not None:
    women_products = []
    women_products += Product.objects.filter(category=women_category, quantity__gt=0)[start:end].values()
    sub_women_categories = Category.objects.filter(parent=women_category)

    if sub_women_categories.count() > 0:
      for item in sub_women_categories:
        products_in_category = Product.objects.filter(category=item, quantity__gt=0)[start:end].values()
        if products_in_category:
          women_products += products_in_category

    products += women_products

  accessory_category = Category.objects.filter(title__iexact='accessories').first()
  if accessory_category is not None:
    accessories = []
    accessories += Product.objects.filter(category=accessory_category, quantity__gt=0)[start:end].values()
    sub_accessory_categories = Category.objects.filter(parent=accessory_category)
    if sub_accessory_categories.count() > 0:
      for item in sub_accessory_categories:
        products_in_category = Product.objects.filter(category=item, quantity__gt=0)[start:end].values()
        if products_in_category:
          accessories += products_in_category

    products += accessories

  return products


def index(request, *args, **kwargs):
  products = get_products_many_category(1, settings.NUM_ITEM)
  wishlist, _ = Wishlist.objects.get_wishlist_or_create(request)
  itemsWishlist = ItemWishlist.objects.filter(wishlist=wishlist)

  for product in products:
    product['is_added_wish'] = False
    for item in itemsWishlist:
      if item.product_id == product['id']:
        product['is_added_wish'] = True
        break

  context = {
    'products': products,
  }
  return render(request, 'index.html', context)


def get_products_of_page(request, page, *args, **kwargs):
  page = int(page)
  if page > 1:
    products = get_products_many_category(page, settings.NUM_ITEM)
    wishlist, _ = Wishlist.objects.get_wishlist_or_create(request)
    itemsWishlist = ItemWishlist.objects.filter(wishlist=wishlist)

    for product in products:
      product['is_added_wish'] = False
      for item in itemsWishlist:
        if item.product_id == product['id']:
          product['is_added_wish'] = True
          break

    data = {
      'status': 'success',
      'products': products,
    }
    return JsonResponse(data)
  else:
    data = {
      'status': 'error',
    }
    return JsonResponse(data)

def search(request, *args, **kwargs):
  keyword = request.GET.get('keyword', None)
  products = None
  if keyword:
    products = Product.objects.filter(Q(title__icontains=keyword) | Q(category__name__icontains=keyword))

  context = {
    'products': products,
  }
  return render(request, 'product.html', context)


def blog(request):
  return render(request, 'blog.html')

def about(request):

  return render(request, 'about.html')

def contact(request):

  return render(request, 'contact.html')

