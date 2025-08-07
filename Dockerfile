FROM ubuntu
ENV TZ="Europe/Zurich"
WORKDIR /

RUN apt update
RUN apt upgrade -y
RUN apt install -y python3-pip python3-requests cron python3-venv

COPY ./requirements.txt .
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

ENV DB_USER=postgres
ENV DB_PORT=5432
ENV DB_HOST=localhost
ENV DB_DATABASE_NAME=postgres

# add cronjob
# RUN echo "* * * * * /opt/venv/bin/python /fetcher.py >> /var/log/cron.log 2>&1" > /etc/cron.d/cron
RUN echo "*/20 7-22 * * * /opt/venv/bin/python /fetcher.py >> /var/log/cron.log 2>&1" > /etc/cron.d/cron
COPY ./fetcher.py .

RUN chmod 0644 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron
RUN chmod +x /fetcher.py
RUN touch /fetcher.log
SHELL ["/bin/bash", "-c"]
CMD cron -f && tail -f fetcher.log