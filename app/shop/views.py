from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from shop.models import Product
from shop.serializers import ProductSerializers

LIST_CACHE_MAX_AGE = 60 * 60
RETRIEVE_CACHE_MAX_AGE = 60 * 60

class ProductView(ModelViewSet):
    queryset = Product.objects.all().prefetch_related('option_set', 'tag_set')
    serializer_class = ProductSerializers

    @method_decorator(cache_page(LIST_CACHE_MAX_AGE))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(RETRIEVE_CACHE_MAX_AGE))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
