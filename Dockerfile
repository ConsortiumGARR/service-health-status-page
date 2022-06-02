FROM python:3.8

RUN apt-get update && apt-get install -y python3-dev
WORKDIR /usr/src/app
COPY ./status_page_app ./status_page_app
COPY ./requirements.txt .
RUN ["pip3", "install", "-r", "requirements.txt"]

COPY ./uWSGI .
EXPOSE 5000
CMD ["uwsgi", "--ini", "app.ini"]
