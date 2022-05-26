# pull official base image
FROM python:3.8.3-alpine
# set work directory
WORKDIR /kanalservice_script
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk --no-cache --update-cache add postgresql-libs postgresql-dev libffi-dev openldap-dev unixodbc-dev git

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .