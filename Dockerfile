FROM python:3.8-slim-buster

LABEL version="1.0"
LABEL description="Base docker image for IoT Service"
LABEL maintainer = ["justintijunel@gmail.com"]

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=iot/app.py
ENV FLASK_ENV=production
EXPOSE 5000

CMD ["flask", "run"]
