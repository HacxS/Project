make a django environment according to you operating system

1. sudo apt-get install python3
2. sudo apt-get install python3-pip
3. sudo apt-get install virtualenv
4. virtualenv -p python3 venv
5. source venv/bin/activate
6. pip install -r requirements.txt
7. django-admin startproject relieve
8. cd relieve
9. python manage.py makemigrations
10. python manage.py migrate
11. python manage.py runserver

Home page URL = localhost:8000/myapp