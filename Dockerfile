FROM python:3.11

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements_full.txt

RUN mkdir /src
COPY ./src /src

WORKDIR /src