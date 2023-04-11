# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


ENV PYTHONPATH "${PYTHONPATH}:./src"
CMD ["python3", "-u", "bin/tester.py", "./config.toml"]
