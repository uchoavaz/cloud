clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "*.log" -exec rm -rf {} \;

deps:
	pip install -r requirements.txt

setup:c
	./manage.py makemigrations
	./manage.py migrate

run:
	./manage.py runserver

restart:

	./manage.py migrate
	./manage.py createsuperuser
user:
	./manage.py createsuperuser

celery:
	./manage.py celery worker --loglevel=info
