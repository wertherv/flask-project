FROM python:3.7

# set a directory for the app
WORKDIR /srv/parser/app

# copy all the files to the container
COPY . .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN set -xe \
    && apt-get update \
    && apt-get install python3-pip

#RUN set -xe
#RUN dnf update
#RUN dnf install python3-pip
    
#RUN pip install --upgrade pip
#RUN pip install uwsgi

RUN pip install --no-cache-dir -r requirements.txt
#EXPOSE 5000
#CMD ["python3", "./app.py"]
#CMD ["uwsgi","--wsgi-file","app.py","--http","5000"]