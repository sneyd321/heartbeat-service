FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn

COPY . .

ENV FLASK_APP=app



#CMD [ "uwsgi",  "--http-socket", "0.0.0.0:8089", "--module", "app:app", "--processes", "2", "--threads",  "4" ]

#CMD ["python", "app.py"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8089", "app:app"]

CMD  [ "celery", "-A", "server.celery", "worker", "-B", "--loglevel=INFO", "--pool=solo", "-O", "fair"]
#Run celery -A server.celery purge to update registry


