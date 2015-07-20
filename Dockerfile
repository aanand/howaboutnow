FROM python:3.4

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD . /code
