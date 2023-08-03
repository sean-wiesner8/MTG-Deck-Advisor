FROM apache/airflow:2.6.3-python3.9

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  && apt-get autoremove -yqq --purge \
  && apt-get -y install libpq-dev gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install terraform
RUN sudo apt-get update && sudo apt-get install -y gnupg software-properties-common && apt-get install -y wget
RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
  gpg --dearmor | \
  sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
RUN gpg --no-default-keyring \
  --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
  --fingerprint
RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
  https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list
RUN sudo apt update && sudo apt-get install -y terraform

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