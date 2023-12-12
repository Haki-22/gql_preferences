# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim-buster as prepare

# instalace curl, aby bylo mozne zprovoznit standardni healthcheck
RUN apt update && apt install curl -y && rm -rf /var/cache/apk/*

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# FROM prepare as tester
#RUN python -m pip install coverage pytest pytest-cov
# RUN python -m unittest tests/*
#RUN python -m pytest --cov-report term-missing --cov=gql_preferences tests/*

FROM prepare as runner
# Creates a non-root user and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--reload=True", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-t", "60", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

## Use an official PostgreSQL image as the base image
#FROM postgres:latest
#FROM python:3.11-slim-buster as prepare
#
## Install any dependencies needed for your application
## (Note: This example assumes your application is a Python app)
#RUN apt-get update && apt-get install -y python3 python3-pip
#
## Set the working directory for your application
#WORKDIR /app
#
## Copy your application code into the container
#COPY . /app
#
## Install Python dependencies for your application
#RUN pip3 install -r requirements.txt
#
## Expose the port your application will run on
#EXPOSE 8000
#
## Set environment variables for PostgreSQL
#ENV POSTGRES_USER postgres
#ENV POSTGRES_PASSWORD example
#ENV POSTGRES_DB data
#
## Command to start your application (customize as needed)
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-t", "60", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
