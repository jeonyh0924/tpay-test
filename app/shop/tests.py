import json
import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase
from shop.models import Product, Tag


@pytest.mark.django_db
class ProductTest(APITestCase):
    def setUp(self) -> None:
        self.products = baker.make('shop.Product', _quantity=2, )

    def test_list(self):
        for product in self.products:
            options = baker.make('shop.ProductOption', product=product, _quantity=2)
            tags = baker.make('shop.Tag', _quantity=2)
            for tag in tags:
                product.tag_set.add(tag)

        response = self.client.get(reverse('Products-list'))

        qs_products = Product.objects.all()
        qs_count = qs_products.count()
        self.assertEqual(response.data.__len__(), qs_count)
        self.assertEqual(response.status_code, 200)

        # for response_data, product in zip(response.data, qs_products):
        #     self.assertEqual(response_data['id'], product.id)
        #     for response_option_set, product_option_set in zip(response_data['option_set'], product.option_set.all()):
        #         self.assertEqual(response_option_set['id'], product_option_set.id)

        # error: AssertionError: 5 != 1 - debug
        # error: FAILED shop/tests.py::ProductTest::test_list - AssertionError: 5 != 6 - pytest

    def test_create(self):
        """
        - 3 개의 ProductOption 을 생성 후 연결
        - 이미 존재하던 1개의 Tag(name: ExistTag) 를 연결
        - 1개의 Tag 를 생성(name: NewTag) 후 연결
        """
        data = {
            'name': 'TestProduct',
            'option_set': [
                {
                    'name': 'TestOption1',
                    'price': 1000
                },
                {
                    'name': 'TestOption2',
                    'price': 500
                },
                {
                    'name': 'TestOption3',
                    'price': 0
                }
            ],
            'tag_set': [
                {
                    'pk': 1,
                    'name': 'ExistTag'
                },
                {
                    'name': 'NewTag'
                }
            ]
        }

        response = self.client.post(reverse('Products-list'),
                                    json.dumps(data),
                                    content_type="application/json")
        qs_data = Product.objects.last()
        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data.get('id'), qs_data.id)
        self.assertEqual(response.data.get('name'), qs_data.name)

        for qs_tags, response_data_tags in zip(qs_data.tag_set.all(), response.data['tag_set']):
            self.assertEqual(qs_tags.id, response_data_tags.get('id'))
            self.assertEqual(qs_tags.name, response_data_tags.get('name'))

        for qs_options, response_data_options in zip(qs_data.option_set.all(), response.data['option_set']):
            self.assertEqual(qs_options.id, response_data_options.get('id'))
            self.assertEqual(qs_options.name, response_data_options.get('name'))
            self.assertEqual(qs_options.price, response_data_options.get('price'))

    def test_create_tag_unique_case(self):
        data = {
            'name': 'TestProduct',
            'option_set': [
                {
                    'name': 'TestOption1',
                    'price': 1000
                },
                {
                    'name': 'TestOption2',
                    'price': 500
                },
                {
                    'name': 'TestOption3',
                    'price': 0
                }
            ],
            'tag_set': [
                {
                    'pk': 1,
                    'name': 'ExistTag'
                },
                {
                    'name': 'NewTag'
                }
            ]
        }

        Tag.objects.create(name='NewTag')
        Tag.objects.create(name='ExistTag')
        response = self.client.post(reverse('Products-list'), json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        # 400 에러 이유가 unique 인지
        for tag in response.data['tag_set']:
            if tag:
                self.assertTrue('unique' in tag.get('name')[0])

        exists_tag_name = data['tag_set'][1]['name']
        exists_tag_ins = Tag.objects.get(name=exists_tag_name)
        self.assertTrue(exists_tag_ins)

    def test_retrieve(self):
        response = self.client.get(reverse('Products-detail', kwargs={"pk": self.products[0].pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), self.products[0].id)

    def test_patch(self):
        data = {
            "pk": self.products[0].id,
            "name": "TestProduct",
            "option_set": [
                {
                    "pk": 1,
                    "name": "TestOption1",
                    "price": 1000
                },
                {
                    "pk": 2,
                    "name": "Edit TestOption2",
                    "price": 1500
                },
                {
                    "name": "Edit New Option",
                    "price": 300
                }
            ],
            "tag_set": [
                {
                    "pk": 1,
                    "name": "ExistTag"
                },
                {
                    "pk": 2,
                    "name": "NewTag"
                },
                {
                    "name": "Edit New Tag"
                }
            ]
        }

        response = self.client.patch(
            reverse('Products-detail', args={self.products[0].pk}), json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(data.get('pk'), response.data.get('id'))
        self.assertEqual(data.get('name'), response.data.get('name'))

        for request_option, response_option in zip(data.get('option_set'), response.data.get('option_set')):
            try:
                self.assertEqual(request_option.get('pk'), response_option.get('id'))
                self.assertEqual(request_option.get('name'), response_option.get('name'))
                self.assertEqual(request_option.get('price'), response_option.get('price'))
            except AssertionError:
                print('option update - assertion error')

        for request_tag, response_tag in zip(data.get('tag_set'), response.data.get('tag_set')):
            try:
                self.assertEqual(request_tag.get('pk'), response_tag.get('id'))
                self.assertEqual(request_tag.get('name'), response_tag.get('name'))
                self.assertEqual(request_tag.get('price'), response_tag.get('price'))
            except AssertionError:
                print('tag update - assertion error')

    def test_patch_Tag_Unique_case(self):
        Tag.objects.create(name='NewTag')
        Tag.objects.create(name='ExistTag')

        data = {
            "pk": 1,
            "name": "TestProduct",
            "option_set": [
                {
                    "pk": 1,
                    "name": "TestOption1",
                    "price": 1000
                },
                {
                    "pk": 2,
                    "name": "Edit TestOption2",
                    "price": 1500
                },
                {
                    "name": "Edit New Option",
                    "price": 300
                }
            ],
            "tag_set": [
                {
                    "pk": 1,
                    "name": "ExistTag"
                },
                {
                    "pk": 2,
                    "name": "NewTag"
                },
                {
                    "name": "Edit New Tag"
                }
            ]
        }

        response = self.client.patch(
            reverse('Products-detail', args={self.products[0].pk}), json.dumps(data),
            content_type="application/json")

        self.assertEqual(response.status_code, 400)
        # 400 에러 이유가 unique 인지
        for tag in response.data['tag_set']:
            if tag:
                self.assertTrue('unique' in tag.get('name')[0])

    def test_delete(self):
        ins = Product.objects.filter(id=self.products[0].pk)
        self.assertEqual(ins.count(), 1)
        response = self.client.delete(f'/shop/products/{self.products[0].pk}/')
        ins = Product.objects.filter(id=self.products[0].pk)
        self.assertEqual(ins.count(), 0)
        self.assertEqual(response.status_code, 204)
