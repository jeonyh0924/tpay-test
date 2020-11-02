## Requirements
- language
	- Python 3.8.2
- framework
	- Django 2.2.12
	
	
## Setup

```https://github.com/jeonyh0924/tpay``` Fork

```shell
# git clone git@github.com:<user id>/backend.git
# cd <폴더 이름>
pyenv virtualenv 3.8.2 <가상환경 이름>
pyenv local <가상환경 이름>

pip install -r requiremens.text
cd app
./manage.py makemigrations
./manage.py migrate
```

