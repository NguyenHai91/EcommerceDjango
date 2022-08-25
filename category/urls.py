
from django.urls import path
from .views import CategoryViewSet, getSubCategories


urlpatterns = [
  path('list/', CategoryViewSet.as_view({'get': 'list'})),
  path('<id_category>/subs/', getSubCategories),
]