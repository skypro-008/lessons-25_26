FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY migrations migrations
COPY default_config.py default_config.py

CMD gunicorn --bind 0.0.0.0:80 --access-logfile='-' --capture-output app:app
