
from django.shortcuts import render
from django.db.models import Q

from category.models import Category
from products.models import Product
from wishlist.models import Wishlist, ItemWishlist


def index(request, *args, **kwargs):
  products = []
  men_category = Category.objects.filter(title__iexact='men').first()
  if men_category is not None:
    men_products = []
    men_products += Product.objects.filter(category=men_category, quantity__gt=0)[:2].values()
    sub_men_categories = Category.objects.filter(parent=men_category)
    if sub_men_categories.count() > 0:
      for item in sub_men_categories:
        products_in_category = Product.objects.filter(category=item, quantity__gt=0)[:2].values()
        if products_in_category:
          men_products += products_in_category

    products += men_products

  women_category = Category.objects.filter(title__iexact='women').first()
  if women_category is not None:
    women_products = []
    women_products += Product.objects.filter(category=women_category, quantity__gt=0)[:2].values()
    sub_women_categories = Category.objects.filter(parent=women_category)

    if sub_women_categories.count() > 0:
      for item in sub_women_categories:
        products_in_category = Product.objects.filter(category=item, quantity__gt=0)[:2].values()
        if products_in_category:
          women_products += products_in_category

    products += women_products

  accessory_category = Category.objects.filter(title__iexact='accessories').first()
  if accessory_category is not None:
    accessories = []
    accessories += Product.objects.filter(category=accessory_category, quantity__gt=0)[:2].values()
    sub_accessory_categories = Category.objects.filter(parent=accessory_category)
    if sub_accessory_categories.count() > 0:
      for item in sub_accessory_categories:
        products_in_category = Product.objects.filter(category=item, quantity__gt=0)[:2].values()
        if products_in_category:
          accessories += products_in_category

    products += accessories

  wishlist, create = Wishlist.objects.get_wishlist_or_create(request)
  wish_items = ItemWishlist.objects.filter(wishlist=wishlist)
  for product in products:
    for item in wish_items:
      if item.product_id == product.id:
        product['is_added_wish'] = True
      else:
        product['is_added_wish'] = False

  context = {
    'products': products,
  }
  return render(request, 'index.html', context)


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

