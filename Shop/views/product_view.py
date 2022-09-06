
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse

from category.models import Category
from products.models import Product


def product_with_category(request, category, *args, **kwargs):
  title_category = str(category).lower()
  category = Category.objects.filter(title__iexact=title_category).first()
  sub_categories = Category.objects.filter(parent=category)

  products = []
  products  += Product.objects.filter(category=category, quantity__gt=0)[:12].values()

  for item in sub_categories:
    products_in_category = Product.objects.filter(category=item, quantity__gt=0)[:12].values()
    if products_in_category:
      products += products_in_category

  context = {
    'products': products,
  }
  return render(request, 'product.html', context)


def product_detail(request, id, *args, **kwargs):
  product = Product.objects.filter(id=id).first()
  if product is not None:
    product.views += 1
    product.save()
    colors = None
    sizes = None
    try:
      sizes = product.sizes.all()
      colors = product.colors.all()
    except:
      pass

    category = Category.objects.get(id=product.category_id)
    related_data = Product.objects.filter(Q(category=product.category) | Q(category__parent_id=category.parent_id))
    related_products = []
    for item in related_data:
      if item.id != product.id:
        related_products.append(item)

    context = {
      'product': product,
      'related_products': related_products,
      'sizes': sizes,
      'colors': colors,
    }
    return render(request, 'product_detail.html', context)

  return render(request, 'product_detail.html')


def product(request, id, *args, **kwargs):
  product = Product.objects.get(id=id)
  if product is not None:
    product.views += 1
    product.save()
    product_obj = {
      'title': product.title,
      'price': product.price,
      'description': product.description,
      'image': product.image.url,
    }

    sizes = product.sizes.all()
    data = {
      'product': product_obj,
      'sizes': sizes,
    }
    return JsonResponse(data)


def product_features(request, *args, **kwargs):
  product_features = Product.objects.filter(featured=True, active=True).order_by('-views')[:12]

  context = {
    'products': product_features,
  }
  return render(request, 'featured.html', context)