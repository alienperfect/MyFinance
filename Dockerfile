FROM python:3.10.7-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /finance

COPY requirements.txt /finance/
RUN pip install -r requirements.txt
COPY . /finance/
