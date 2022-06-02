FROM alpine:3.16

RUN apk add --no-cache \
    uwsgi-python3 \
    python3 \
    py3-pip
    
RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1
WORKDIR /usr/src/app
COPY ./status_page_app ./status_page_app
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./uWSGI .
EXPOSE 5000
CMD ["uwsgi", "--ini", "app.ini"]
