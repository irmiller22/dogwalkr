FROM python:3.8.2-slim-buster

RUN apt-get -y update \
    && apt-get -y install build-essential \
    curl \
    git \
    nodejs \
    npm \
    postgresql-client \
    python3-dev \
    && apt-get clean \
    && npm install pyright@1.1.45

COPY src/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY alembic /dogwalkr/alembic
COPY bin /dogwalkr/bin
COPY src /dogwalkr/src
COPY sql /dogwalkr/sql
COPY alembic.ini /dogwalkr/.

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/dogwalkr/src"

WORKDIR /dogwalkr
