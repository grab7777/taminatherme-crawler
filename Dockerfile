FROM ubuntu
WORKDIR /
COPY ./fetcher.py .
COPY ./requirements.txt .

RUN apt update
RUN apt upgrade -y
RUN apt install -y python3-pip python3-requests cron python3-venv
# TODO: pyppeteer does not work correctly, change to playwright
# dependencies for puppeteer
# RUN apt install -y ca-certificates fonts-liberation libatk-bridge2.0-0 libatk1.0-0 \
                #    libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 \
                #    libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 \
                #    libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 \
                #    libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget \
                #    xdg-utils

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt
RUN playwright install

ENV DB_USER=postgres
ENV DB_PORT=5432
ENV DB_HOST=localhost
ENV DB_DATABASE_NAME=postgres

# add cronjob
COPY ./cron /etc/cron.d/cron

RUN chmod 0644 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron
RUN chmod +x /fetcher.py
RUN touch /cron_task.log
SHELL ["/bin/bash", "-c"]
CMD cron -f && tail -f cron_task.log