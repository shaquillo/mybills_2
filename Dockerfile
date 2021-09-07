# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8-alpine

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV PATH='/scripts:${PATH}'

# Get the Real World example app
#RUN git clone https://github.com/gothinkster/django-realworld-example-app.git /bills_app

# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /bills_api
COPY . /bills_api
WORKDIR /bills_api
RUN mv scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/files/media
RUN mkdir -p /vol/files/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chown -R 755 /vol/files
USER user

#VOLUME /drf_src
#
#EXPOSE 9800
#
#CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]

CMD ["entrypoint.sh"]
