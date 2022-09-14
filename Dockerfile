FROM python:3.10.7-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /fincance

COPY requirements.txt /fincance/
RUN pip install -r requirements.txt
COPY . /fincance/

EXPOSE 8000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000