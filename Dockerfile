FROM ubuntu
WORKDIR /
COPY ./fetcher.py .
COPY ./requirements.txt .

RUN apt update
RUN apt install -y python3-pip python3-requests cron 

# dependencies for puppeteer
RUN apt install -y ca-certificates
RUN apt install -y fonts-liberation
RUN apt install -y libasound2
RUN apt install -y libatk-bridge2.0-0
RUN apt install -y libatk1.0-0
RUN apt install -y libc6
RUN apt install -y libcairo2
RUN apt install -y libcups2
RUN apt install -y libdbus-1-3
RUN apt install -y libexpat1
RUN apt install -y libfontconfig1
RUN apt install -y libgbm1
RUN apt install -y libgcc1
RUN apt install -y libglib2.0-0
RUN apt install -y libgtk-3-0
RUN apt install -y libnspr4
RUN apt install -y libnss3
RUN apt install -y libpango-1.0-0
RUN apt install -y libpangocairo-1.0-0
RUN apt install -y libstdc++6
RUN apt install -y libx11-6
RUN apt install -y libx11-xcb1
RUN apt install -y libxcb1
RUN apt install -y libxcomposite1
RUN apt install -y libxcursor1
RUN apt install -y libxdamage1
RUN apt install -y libxext6
RUN apt install -y libxfixes3
RUN apt install -y libxi6
RUN apt install -y libxrandr2
RUN apt install -y libxrender1
RUN apt install -y libxss1
RUN apt install -y libxtst6
RUN apt install -y lsb-release
RUN apt install -y wget
RUN apt install -y xdg-utils

RUN pip3 install -r ./requirements.txt

# add cronjob
COPY ./cron /etc/cron.d/cron
RUN chmod 0644 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron
RUN chmod +x /fetcher.py
RUN touch /cron_task.log
CMD ["cron" , "-f"]