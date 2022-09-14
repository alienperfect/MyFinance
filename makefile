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