from django.urls import path

from .views import CartAPIView, CheckProductInCart

urlpatterns = [
    path('', CartAPIView.as_view()),
    path('add/', CartAPIView.as_view()),
    path('delete/', CartAPIView.as_view()),
    path('update/', CartAPIView.as_view()),
    path('<product_id>/', CheckProductInCart.as_view()),
]
