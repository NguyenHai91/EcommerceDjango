
from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product, Size

User = get_user_model()


class WishlistManager(models.Manager):
  def get_wishlist_or_create(self, request):
    created = False
    wishlist_id = request.session.get('wish_id')

    if request.user.is_authenticated:
      if self.model.objects.filter(user__email=request.user).count() == 1:
        wishlist = self.model.objects.get(user__email=request.user)
        return wishlist, created
      elif wishlist_id is not None:
        if self.model.objects.filter(id=wishlist_id, user=request.user).count() == 0:
          wishlist = self.model.objects.get(id=wishlist_id)
          wishlist.user = request.user
          wishlist.save()
          return wishlist, created
      else:
        wishlist = self.model.objects.create(user=request.user)
        created = True
        request.session['wish_id'] = wishlist.id
        return wishlist, created
    if wishlist_id is not None:
      if self.model.objects.filter(id=wishlist_id).count() == 1:
        wishlist = self.model.objects.get(id=wishlist_id)
        return wishlist, created

    wishlist = self.model.objects.create()
    created = True
    request.session['wish_id'] = wishlist.id
    return wishlist, created



class Wishlist(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  objects = WishlistManager()

  @property
  def count_items(self):
    return len(self.wishlist_items.all())


class ItemWishlist(models.Model):
  wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_items')
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  objects = models.Manager()
