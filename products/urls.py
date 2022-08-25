
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ProductViewSet, RelatedProductView, ProductAPIView,
                    getProductsWithCategory, getManyProductsDifferWithCategory,
                    getProductWithNameCategory, getProductsNewest,
                    getProductsHighView, getProductsBestSeller)

urlpatterns = [
  path('create/', ProductAPIView.as_view()),
  path('delete/<id>/', ProductViewSet.as_view({'delete': 'destroy'})),
  path('update/<id>/', ProductViewSet.as_view({'put': 'update'})),
  path('list/', ProductAPIView.as_view()),
  path('<int:id>/', ProductViewSet.as_view({'get': 'retrieve'})),
  path('related/<id>/', RelatedProductView.as_view()),
  path('category/<name_category>/', getProductWithNameCategory),
  path('category/<int:id_category>/details/', getProductsWithCategory),
  path('category/<int:id_category>/', getManyProductsDifferWithCategory),
  path('newest/', getProductsNewest),
  path('high-view/', getProductsHighView),
  path('bestseller/', getProductsBestSeller),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)