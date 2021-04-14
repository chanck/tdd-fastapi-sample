# pull official base image
FROM python:3.8.1-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt
# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip
# copy project
COPY . /usr/src/app/
# Optional to serve FASTAPI through uvicorn
# If you build and run the container from docker-compose you do not need the below 2 lines (expose & cmd) comment them.
# If you build and run the container from docker command leave the below 2 line uncomment
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]