from django.contrib import admin
from .models import BillingProfile, Payment

admin.site.register(Payment)
admin.site.register(BillingProfile)