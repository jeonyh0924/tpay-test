from django.urls import path
from rest_framework import routers

from shop.views import ProductView

router = routers.SimpleRouter()

router.register('products', ProductView, basename='Products')

shop_urlpatterns = router.urls
