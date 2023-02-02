FROM python:3.11.1-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip pipenv

WORKDIR /backend
COPY ./Pipfile* ./
RUN pipenv sync

COPY . .

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]