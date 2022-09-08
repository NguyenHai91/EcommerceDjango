from django.contrib import admin
from django import forms

from .models import Product, Tag, Size, Color, ImageProduct


class ProductAdminForm(forms.ModelForm):
  image = forms.FileField(
    widget=forms.ClearableFileInput(attrs={'multiple': True}),
    label='image',
    required=False,
  )

  class Meta:
    model = Product
    fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
  readonly_fields = ['sold', 'views']
  list_display = ['id', '__str__', 'timestamp', 'category', 'quantity', 'original_price',
                    'price', 'gender', 'featured', 'image']
  form = ProductAdminForm

  class meta:
    model = Product
    ordering = ['-id', 'timestamp']

  def save_model(self, request, obj, form, change):
    # instance = form.save(commit=False)
    # instance.save(request=request)
    # return instance
    list_images = request.FILES.getlist('image', False)
    obj.image = list_images[0]
    obj.save()
    if list_images and len(list_images) > 1:
      for img in list_images[1:]:
        ImageProduct.objects.create(product=obj, image=img)
    return super().save_model(request, obj, form, change)


class ImageProductAdmin(admin.ModelAdmin):
  list_display = ['id', '__str__', 'created_date']
  class meta:
    model = ImageProduct
    ordering = ['-id', '-created_date']


class SizeAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'code_size']
  class meta:
    model = Size


admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color)
admin.site.register(ImageProduct, ImageProductAdmin)
