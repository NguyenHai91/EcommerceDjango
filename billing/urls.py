from django.urls import path

from .views import BillingProfileAPIView

urlpatterns = [
    path('', BillingProfileAPIView.as_view()),
]
