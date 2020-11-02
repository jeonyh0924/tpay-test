from rest_framework.test import APITestCase


class ProductTest(APITestCase):
    def setUp(self) -> None:
        pass

    def test_create(self):
        """
        - 3 개의 ProductOption 을 생성 후 연결
        - 이미 존재하던 1개의 Tag(name: ExistTag) 를 연결
        - 1개의 Tag 를 생성(name: NewTag) 후 연결
        """
        data = {
            "name": "TestProduct",
            "option": [
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
            "tag": [
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
