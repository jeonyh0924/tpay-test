from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer
from datetime import datetime

from shop.models import Product, ProductOption, Tag


class TagSerializers(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProductOptionSerializers(ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('id', 'name', 'price')


class ProductSerializers(WritableNestedModelSerializer):
    option = ProductOptionSerializers(many=True)
    tag = TagSerializers(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'option', 'tag')

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        start = datetime.now()
        data = self.context.get('request').data

        # Product option
        option_pk_list = []
        option_update_bulk_list = []
        for option in data['option_set']:
            if option.get('pk'):
                option_pk_list.append(option['pk'])
                ins = ProductOption.objects.get(pk=option['pk'])

                # bulk update
                ins.name = option['name']
                ins.price = option['price']
                ins.save()
            else:
                # bulk create
                created_option = ProductOption.objects.create(name=option['name'], price=option['price'],
                                                              product=instance)
                option_pk_list.append(created_option.pk)
        delete_options_ins = instance.option.exclude(pk__in=option_pk_list)

        for option_ins in delete_options_ins:
            # bulk delete
            option_ins.delete()

        # Tag
        tag_pk_list = []
        for tag in data['tag_set']:
            if tag.get('pk'):
                tag_pk_list.append(tag['pk'])

                ins = Tag.objects.get(pk=tag['pk'])
                ins.name = tag['name']
                ins.save()
            else:
                tag_ins = Tag.objects.filter(name=tag['name'])
                if len(tag_ins) == 0:
                    created_tag = Tag.objects.create(name=tag['name'])
                    tag_pk_list.append(created_tag.pk)
                    instance.tag.add(created_tag)
                elif len(tag_ins) == 1:
                    if not instance.tag.get(name=tag_ins[0].name):
                        instance.tag.add(tag_ins[0])
                        tag_pk_list.append(tag_ins[0].pk)

        delete_tag_ins = instance.tag.exclude(pk__in=tag_pk_list)
        for tag_ins in delete_tag_ins:
            tag_ins.delete()
        print(datetime.now() - start)
        return instance
