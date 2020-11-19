# Contents
1. Requirements
2. Set up
3. docker compose
4. testcode
5. API 테스트 방법, PostMan URL


## Requirements
- language
	- Python 3.8.2
- framework
	- Django 2.2.12
	
	
## Setup

```shell script
# git clone git@github.com:jeonyh0924/tpay-test.git <ROOT DIR NAME>
# cd <ROOT DIR>

docker build -t tpay -f Dockerfile .
docker run --rm -it -p 8000:80 --name tpay tpay

```


## ~~docker compose~~

```shell script
# 기존에 동작하고 있는 docker-compose 가 있다면
#docker-compose down

# 시작 //
# file: <ROOT DIR>/
docker-compose up -d


cd app

./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

### API 테스트 방법, PostMan URL

- https://documenter.getpostman.com/view/5847490/TVYQ1Z4s

```shell
# Root DIR/app
./manage.py test

# Root dir/app
pytest
```

- Postman Export > tpay-test/tpay.postman_collection.json
