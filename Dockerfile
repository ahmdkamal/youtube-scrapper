FROM python:2.7

RUN apt-get update && apt-get install -y wget

WORKDIR /usr/src/app

EXPOSE 5000

COPY requirements.txt ./

RUN apt-get install -y libxml2-dev libxslt-dev gcc

RUN apt-get install -y libxml2 g++ build-essential libssl-dev libffi-dev python-dev

RUN python -m pip install --user --no-cache-dir -r requirements.txt

COPY . .

