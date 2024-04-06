FROM python:3.12
COPY webapp.py /app/
COPY gunicorn_config.py /app/
COPY requirements.txt /
COPY templates /app/templates
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
EXPOSE 8080
ENTRYPOINT [ "gunicorn", "--config", "gunicorn_config.py", "webapp:app" ]