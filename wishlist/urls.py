
from django.urls import path, include
from rest_framework import routers

from .views import WishlistView


router = routers.DefaultRouter()
# router.register('wishlist/', WishlistView)

urlpatterns = [
  path('', WishlistView.as_view()),
  path('add/', WishlistView.as_view()),
  path('delete/', WishlistView.as_view()),
]
urlpatterns += router.urls