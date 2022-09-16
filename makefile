run:
	py manage.py runserver

test:
	py manage.py test

shell:
	py manage.py shell_plus

mm:
	py manage.py makemigrations
	py manage.py migrate

clean:
	py manage.py reset_db

docker-run:
	docker-compose up

docker-build:
	docker-compose build

docker-shell:
	docker exec -it finance_web python manage.py shell_plus

