FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE $PORT

CMD exec gunicorn --bind 0.0.0.0:${PORT:-8000} config.wsgi:application
