from django.contrib import admin

from .models import Product, Tag, Size, Color, ImageProduct


class ProductAdmin(admin.ModelAdmin):
  readonly_fields = ['sold', 'views']
  list_display = ['__str__', 'id', 'timestamp', 'category', 'quantity', 'original_price',
                    'price', 'gender', 'featured', 'image']

  class meta:
    model = Product


class ImageProductAdmin(admin.ModelAdmin):
  list_display = ['__str__', 'id', 'created_date']

  class meta:
      model = ImageProduct


class SizeAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'code_size']

  class meta:
    model = Size

admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color)
admin.site.register(ImageProduct, ImageProductAdmin)
