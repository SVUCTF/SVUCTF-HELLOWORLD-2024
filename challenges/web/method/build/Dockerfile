FROM python:3.12-alpine

WORKDIR /app

RUN pip install --no-cache-dir flask gunicorn

COPY main.py /app/

CMD ["gunicorn", "main:app", "-b", "0.0.0.0:80"]
