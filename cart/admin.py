from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'used', 'timestamp', 'updated']

  class meta:
    model = Cart


class CartItemAdmin(admin.ModelAdmin):
  list_display = ['id', 'cart', 'product', 'quantity']

  class meta:
    model = CartItem


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
