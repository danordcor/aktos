FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE $PORT

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
