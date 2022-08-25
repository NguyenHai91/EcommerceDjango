
from django.contrib import admin

from .models import Category
# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'parent']

  class meta:
    model = Category

admin.site.register(Category, CategoryAdmin)