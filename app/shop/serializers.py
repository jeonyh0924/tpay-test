
from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin
from rest_framework.serializers import ModelSerializer

from shop.models import Product, ProductOption, Tag


class TagSerializers(UniqueFieldsMixin):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProductOptionSerializers(ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('id', 'name', 'price')


class ProductSerializers(WritableNestedModelSerializer):
    option_set = ProductOptionSerializers(many=True)
    tag_set = TagSerializers(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'option_set', 'tag_set')
