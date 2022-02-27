FROM python:3.10.0b3

WORKDIR /code

COPY ./requirements/base.txt requirements/base.txt
COPY ./requirements/production.txt requirements/production.txt
RUN pip install --upgrade pip && pip install -r requirements/production.txt

ADD . /code

ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
