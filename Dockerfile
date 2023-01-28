FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    gcc

COPY poetry.lock pyproject.toml /app/

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

COPY . /app

RUN poetry shell
RUN poetry install --no-interaction --no-dev

ENTRYPOINT ["python", "iot/app.py"]