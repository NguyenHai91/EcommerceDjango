
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

from products.models import Product

User = get_user_model()


class Payment(models.Model):
  STATUS = (('Valid', 'Valid'), ('Invalid', 'Invalid'))
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  payment_id = models.CharField(max_length=100)
  payment_method = models.CharField(max_length=250)
  amount_paid = models.CharField(max_length=100)
  status = models.CharField(max_length=100, choices=STATUS, default='Valid')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = models.Manager()


class BillingProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class BillingProfile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField()
  phone = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  timestamp = models.DateTimeField(auto_now_add=True)

  objects = BillingProfileManager()

  def __str__(self):
      return self.email


def billing_profile_created_receiver(sender, instance: BillingProfile, created, *args, **kwargs):
    pass


post_save.connect(billing_profile_created_receiver, sender=BillingProfile)

