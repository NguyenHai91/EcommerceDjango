from django.contrib import admin

from wishlist.models import Wishlist, ItemWishlist

# Register your models here.

class WishlistAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'timestamp', 'updated']

  class meta:
    model = Wishlist


admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ItemWishlist)