FROM ubuntu
WORKDIR /
COPY ./fetcher.py .
COPY ./requirements.txt .
# ENV PYTHONUNBUFFERED=1
# RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
# RUN apk add py3-pip
# RUN py3-pip install --no-cache --upgrade pip setuptools
# RUN python3 -m venv ~/venv
# RUN . ~/venv/bin/activate
RUN apt update
RUN apt install -y python3-pip python3-requests cron 


# RUN apt install -y libx11-xcb1
# RUN apt install -y libxcomposite-dev
# RUN apt install -y libxcursor-dev
# RUN apt install -y libxdamage-dev
# RUN apt install -y libxfixes-dev
# RUN apt install -y libxi-dev
# RUN apt install -y libxrender-dev
# RUN apt install -y libnss3-dev
# RUN apt install -y libnspr4-dev
# RUN apt install -y libcups2-dev
# RUN apt install -y libxss-dev
# RUN apt install -y libxrandr-dev
# RUN apt install -y libasound-dev
# RUN apt install -y libpangocairo-1.0-0
# RUN apt install -y libpango1.0-dev
# RUN apt install -y libcairo-dev
# RUN apt install -y libatk1.0-0
# RUN apt install -y libatk-bridge2.0-dev
# RUN apt install -y libgtk-3.so.0
# RUN apt install -y libgdk-3.so.0
# RUN apt install -y libgdk-pixbuf2.0-dev
RUN pip3 install -r ./requirements.txt

# RUN apk add py3-dotenv
# RUN apk add py3-psycopg2
# RUN apk add py3-selenium

# add cronjob
RUN echo '*  *  *  *  *    python3 ./fetcher.py' > /etc/crontab
RUN chmod +x ./fetcher.py
RUN touch ./cron_task.log
CMD cron && tail -f ./cron_task.log