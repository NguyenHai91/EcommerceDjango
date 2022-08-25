
from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product, Size, Color
from wishlist.models import Wishlist


User = get_user_model()


class CartManager(models.Manager):
  def get_existing_or_new(self, request, *args, **kwargs):
    created = False
    cart_id = request.session.get('cart_id', None)

    if request.user.is_authenticated:
      if self.model.objects.filter(user__email=request.user, used=False).count() == 1:
        cart = self.model.objects.get(user__email=request.user, used=False)
        return cart, created
      elif cart_id is not None:
        if self.model.objects.filter(id=cart_id, user=request.user, used=False).count() == 0:
          cart = self.model.objects.get(id=cart_id)
          cart.user = request.user
          cart.save()
          return cart, created
      else:
        cart = self.model.objects.create(user=request.user)
        created = True
        request.session['cart_id'] = cart.id
        return cart, created

    if cart_id is not None:
      if self.model.objects.filter(id=cart_id, used=False).count() == 1:
        cart = self.model.objects.get(id=cart_id)
        return cart, created

    cart = self.model.objects.create()
    created = True
    request.session['cart_id'] = cart.id
    return cart, created


class Cart(models.Model):
  user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
  used = models.BooleanField(default=False)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  objects = CartManager()

  @property
  def amount(self):
    amount = 0
    try:
      for item in self.cart_items.all():
        amount += int(item.quantity) * float(item.product.price)
    except:
      pass
    return round(amount, 2)

  @property
  def tax_total(self):
    total = 0
    try:
      for item in self.cart_items.all():
        total += int(item.quantity) * float(item.product.price) * \
                 float(item.product.tax) / 100
    except:
      pass
    return round(total, 2)

  @property
  def num_item(self):
    num_item = 0
    try:
      for item in self.cart_items.all():
        num_item += item.quantity
    except:
      pass
    return num_item

  @property
  def total_amount(self):
    total = 0
    try:
      for item in self.cart_items.all():
        total += int(item.quantity) * float(item.product.price)
    except:
      pass
    total += self.tax_total
    return round(total, 2)


class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
  color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
  quantity = models.IntegerField(default=0)
  price = models.CharField(max_length=100)
  sale = models.CharField(max_length=50, null=True, blank=True)

