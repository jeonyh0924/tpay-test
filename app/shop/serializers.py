from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer

from shop.models import Product, ProductOption, Tag


class TagSerializers(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'validators': []},
        }


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

    # def update(self, instance, validated_data):
    #     data = self.context.get('request').data
    #
    #     # Product option
    #     option_id_list = []
    #     option_bulk_create_list = []
    #     for option in data['option_set']:
    #         if option.get('pk'):
    #             option_id_list.append(option['pk'])
    #
    #             ins = ProductOption.objects.get(pk=option['pk'])
    #             if (ins.name != option['name']) or (ins.price != option['price']):
    #                 ins.name, ins.price = option['name'], option['price']
    #                 ins.save()
    #         else:
    #             # bulk create
    #             option_bulk_create_list.append(
    #                 ProductOption(name=option['name'], price=option['price'], product=instance))
    #
    #             for ins in ProductOption.objects.bulk_create(option_bulk_create_list):
    #                 option_id_list.append(ins.id)
    #
    #     delete_options_ins = instance.options.exclude(id__in=option_id_list)
    #
    #     ProductOption.objects.filter(id__in=delete_options_ins).delete()
    #
    #     # Tag
    #     tag_id_list = []
    #     for tag in data['tag_set']:
    #         if tag.get('pk'):
    #             tag_id_list.append(tag['pk'])
    #
    #             ins = Tag.objects.get(id=tag['pk'])
    #             ins.name = tag['name']
    #             ins.save()
    #         else:
    #             created_ins = Tag.objects.create(name=tag['name'])
    #             tag_id_list.append(created_ins.id)
    #
    #     delete_tag_ins = instance.tag.exclude(id__in=tag_id_list)
    #     for tag_ins in delete_tag_ins:
    #         tag_ins.delete()
    #     return instance
