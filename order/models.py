from django.db import models
from django.db.models.signals import post_save, pre_save

from billing.models import BillingProfile
from cart.models import Cart
from Shop.utils import unique_product_id_generator

STATUS_CHOICES = (
  ('created', 'Created'),
  ('paid', 'Paid'),
  ('shipping', 'Shipping'),
  ('delivered', 'Delivered'),
  ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter()

  def get_order(self, billing_profile: BillingProfile):
    qs = self.get_queryset().filter(
      billing_profile__user=billing_profile.user, status='created')
    if qs.count() == 0:
      cart = billing_profile.user.cart_set.filter(used=False).first()
      order = Order(billing_profile=billing_profile, cart=cart)
      order.save()
      return order
    else:
      order = qs.first()
      order.billing_profile = billing_profile
      order.save()
      return order


class Order(models.Model):
  order_code = models.CharField(max_length=200)
  billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  active = models.BooleanField(default=True)
  status = models.CharField(choices=STATUS_CHOICES, default='created', max_length=120)
  shipping_fee = models.DecimalField(default=70, max_digits=10, decimal_places=2)
  amount = models.DecimalField(default=70, max_digits=10, decimal_places=2)
  tax = models.DecimalField(default=70, max_digits=10, decimal_places=2)
  total_amount = models.DecimalField(default=70, max_digits=10, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)

  objects = OrderManager()

  def cal_amount(self):
    self.amount = float(self.cart_total) + float(self.tax_total) + float(self.shipping_fee)
    return self.amount

  def cal_tax(self):
    self.tax = self.cart.tax_total
    return self.tax

  def cal_total_pay(self):
    amount = float(self.cart_total) + float(self.tax_total) + float(self.shipping_fee)
    self.total_amount = round(amount)
    return self.total_amount

  def check_done(self):
    billing_profile = self.billing_profile
    total = self.total
    cart = self.cart
    active = self.active
    if active and total > 0 and cart and billing_profile:
      return True
    return False

  def mark_paid(self):
    if self.check_done():
      self.cart.used = True
      self.cart.save()
      self.status = 'paid'
      self.save()
      return True
    return False


def pre_save_create_order_code(sender, instance, *args, **kwargs):
  if not instance.order_code:
    instance.order_code = unique_product_id_generator(instance)


pre_save.connect(pre_save_create_order_code, sender=Order)
