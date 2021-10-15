FROM python:3.9.7

# RUN apt-get update && \
#     apt-get -y install supervisor

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

ADD . /app
WORKDIR /app

EXPOSE 8000
