from model_bakery import baker
from rest_framework.test import APITestCase

from shop.models import Product


class ProductTest(APITestCase):
    def setUp(self) -> None:
        self.products = baker.make('shop.Product', _quantity=2, )

    def test_list(self):
        for product in self.products:
            options = baker.make('shop.ProductOption', product=product, _quantity=2)
            tags = baker.make('shop.Tag', _quantity=2)
            for tag in tags:
                product.tag_set.add(tag)

        response = self.client.get('/shop/products/')
        qs_count = Product.objects.count()
        self.assertEqual(response.data.__len__(), qs_count)
        self.assertEqual(response.status_code, 200)

        for response_data, product in zip(response.data, self.products):
            self.assertEqual(response_data['id'], product.id)
            for response_option_set, product_option_set in zip(response_data['option_set'], product.option_set.all()):
                self.assertEqual(response_option_set['id'], product_option_set.id)

    def test_create(self):
        """
        - 3 개의 ProductOption 을 생성 후 연결
        - 이미 존재하던 1개의 Tag(name: ExistTag) 를 연결
        - 1개의 Tag 를 생성(name: NewTag) 후 연결
        """
        data = {
            "name": "TestProduct",
            "option_set": [
                {
                    "name": "TestOption1",
                    "price": 1000
                },
                {
                    "name": "TestOption2",
                    "price": 500
                },
                {
                    "name": "TestOption3",
                    "price": 0
                }
            ],
            "tag_set": [
                {
                    "pk": 1,
                    "name": "ExistTag"
                },
                {
                    "name": "NewTag"
                }
            ]
        }
        response = self.client.post('/shop/products/', data=data)

        self.assertEqual(response.status_code, 201)
        self.fail()

    def test_retrieve(self):
        response = self.client.get(f'/shop/products/{self.products[0].pk}/')
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
        response = self.client.patch(f'/shop/products/{self.products[0].pk}/', data=data)
        self.assertEqual(response.status_code, 200)
        self.fail()

    def test_delete(self):
        ins = Product.objects.filter(id=self.products[0].pk)
        self.assertEqual(ins.count(), 1)
        response = self.client.delete(f'/shop/products/{self.products[0].pk}/')

        ins = Product.objects.filter(id=self.products[0].pk)
        self.assertEqual(ins.count(), 0)
        self.assertEqual(response.status_code, 204)
