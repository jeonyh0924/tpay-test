from django.urls import path
from rest_framework_nested import routers

from shop.views import ProductView

router = routers.SimpleRouter()

router.register('products', ProductView)

shop_urlpatterns = router.urls
