from rest_framework.viewsets import ModelViewSet

from shop.models import Product
from shop.serializers import ProductSerializers


class ProductView(ModelViewSet):
    queryset = Product.objects.all().prefetch_related('option', 'tag')
    serializer_class = ProductSerializers
