FROM python:3.9.5-slim

RUN mkdir instance
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY app ./app

EXPOSE 80