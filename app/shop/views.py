from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shop.models import Product
from shop.serializers import ProductSerializers


class ProductView(ModelViewSet):
    queryset = Product.objects.all().prefetch_related('option_set', 'tag_set')
    serializer_class = ProductSerializers

    def create(self, request, *args, **kwargs):
        kwargs['many'] = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
