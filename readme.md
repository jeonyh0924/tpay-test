## Requirements
- language
	- Python 3.8.2
- framework
	- Django 2.2.12
	
	
## Setup

```shell
# git clone git@github.com:jeonyh0924/tpay-test.git
# cd <폴더 이름>
pyenv virtualenv 3.8.2 <가상환경 이름>
pyenv local <가상환경 이름>

pip install -r requiremens.text

export DJANGO_SETTINGS_MODULE=config.settings.dev

cd app

./manage.py makemigrations
./manage.py migrate
```


### docker compose 

```shell
# 기존에 동작하고 있는 docker-compose 가 있다면
#docker-compose down

# 시작 //
# file: tpay-test/
docker-compose up -d

export DJANGO_SETTINGS_MODULE=config.settings.dev


cd app

./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```