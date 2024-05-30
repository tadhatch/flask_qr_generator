FROM python:3.12
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -y unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99
COPY webapp.py /app/
COPY gunicorn_config.py /app/
COPY requirements.txt /
COPY templates /app/templates
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
EXPOSE 8080
ENTRYPOINT [ "gunicorn", "--config", "gunicorn_config.py", "webapp:app" ]