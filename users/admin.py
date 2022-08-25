from django.contrib import admin
from .models import MyUser, ProfileUser

admin.site.register(MyUser)
admin.site.register(ProfileUser)