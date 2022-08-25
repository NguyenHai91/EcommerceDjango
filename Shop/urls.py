"""Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from .views import (index_view, cart_view, product_view, user_view, wish_view, order_view)



urlpatterns = [
    path('admin/', admin.site.urls),
    # api
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/category/', include('category.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/checkout/', include('billing.urls')),
    path('api/wishlist/', include('wishlist.urls')),
    
    # template
    path('', index_view.index),
    path('search/', index_view.search),
    path('products/category=<category>/', product_view.product_with_category),
    path('product/detail/id=<int:id>/', product_view.product_detail),
    path('product/id=<int:id>/', product_view.product), # ajax request product
    path('features/', product_view.product_features),
    path('blog/', index_view.blog),
    path('about/', index_view.about),
    path('contact/', index_view.contact),
    re_path(r'^login(.*?)$', user_view.login_user),
    path('logout/', user_view.logout_user),
    path('register/', user_view.register),
    path('cart/', cart_view.cart),
    path('add-cart/id=<id>/quantity=<int:quantity>/', cart_view.add_cart),
    path('cart/delete/id=<id>/', cart_view.delete_item),
    path('cart/update/id_item=<id>/', cart_view.update_cart),
    path('wish/', wish_view.wishlist),
    path('wish/add/id=<id_product>/', wish_view.add_wish),
    path('wish/delete/id=<id_item>/', wish_view.delete_wish),
    path('order/', order_view.order, name='order'),
    path('checkout/', order_view.checkout),
    path('success/', order_view.success, name='success'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

