FROM python:3.6.8

RUN apt-get update && apt-get install -y vim libgl1-mesa-glx;

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

ADD requirements.txt /code

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /code

RUN chmod +x *.sh
