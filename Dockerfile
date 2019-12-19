FROM python:3.8-slim-buster

RUN apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY start_server.sh /start_server.sh
RUN chmod +rwx /start_server.sh
COPY ./ /nx_server
RUN  ls -l /nx_server

ENTRYPOINT ["/start_server.sh"]