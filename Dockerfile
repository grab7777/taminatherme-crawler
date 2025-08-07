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
# RUN echo "* * * * * /opt/venv/bin/python3 /fetcher.py >> /var/log/cron.log 2>&1" > /etc/cron.d/cron
RUN echo "* * * * * /execute.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/cron
# RUN echo "*/20 7-22 * * * /opt/venv/bin/python /fetcher.py >> /var/log/cron.log 2>&1" > /etc/cron.d/cron
COPY ./fetcher.py .
COPY .env .
COPY ./execute.sh .

RUN chmod 0644 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron
RUN chmod +x /fetcher.py
RUN chmod +x /execute.sh
RUN touch /fetcher.log && touch /var/log/cron.log
USER root
SHELL ["/bin/bash", "-c"]
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
# CMD cron -f && tail -f /var/log/cron.log
# CMD ["/opt/venv/bin/python", "fetcher.py"]