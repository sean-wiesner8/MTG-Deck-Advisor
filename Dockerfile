FROM --platform=linux/amd64 apache/airflow:2.6.3-python3.9

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  && apt-get autoremove -yqq --purge \
  && apt-get -y install libpq-dev gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# RUN apt-get update \
#   && apt-get install -y wget \
#   && rm -rf /var/lib/apt/lists/*
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
#   && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# RUN apt-get update && apt-get -y install google-chrome-stable

# install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
# ENV DISPLAY=:99

USER airflow

COPY /Pipfile /Pipfile
COPY /Pipfile.lock /Pipfile.lock

# Dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt