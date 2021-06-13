FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD  [ "celery", "-A", "server.celery", "worker", "-B", "--loglevel=INFO", "--pool=solo", "-O", "fair"]
#Run celery -A server.celery purge to update registry
#CMD ["python", "app.py"]

