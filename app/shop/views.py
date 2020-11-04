from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shop.models import Product
from shop.serializers import ProductSerializers


class ProductView(ModelViewSet):
    queryset = Product.objects.all().prefetch_related('option_set', 'tag_set')
    serializer_class = ProductSerializers

    def list(self, request, *args, **kwargs):
        cache_key = request._request.path_info

        cache_data = cache.get(cache_key, None)
        if not cache_data:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            cache_data = serializer.data
            cache.set(cache_key, cache_data, 60 * 60)

        return Response(cache_data)

    def create(self, request, *args, **kwargs):
        kwargs['many'] = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, **kwargs)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        cache_key = kwargs.get('pk', None)

        cache_data = cache.get(cache_key, None)
        if not cache_data:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            cache_data = serializer.data
            cache.set(cache_key, cache_data, 60 * 60)
        return Response(cache_data)
