# Taminatherme Crawler

Author: grab777
Updated: 28.01.2024

## Setup

### Prerequisites

- you need a running PostgreSQL Database to send the crawled data to.

### Create the docker container

1. Download the repository with `git clone https://github.com/grab7777/taminatherme-crawler.git`
1. Copy the example.env, rename it to .env and add all required information
1. Make a new file called db_password.txt and insert the database password
1. You can change the cron timings in the file `cron`
1. create the container with `docker image build -t taminatherme-crawler:latest .`
1. If you get `cron` errors: Make sure the cron file is written with `LF` at the end, not `CRLF`!
1. make sure, docker swarm is enabled (`docker info`)

   ![docker info](image.png)

1. if not: `docker swarm init`

## Changelog

The most important changes are logged here:

| Date       | Changes       |
| ---------- | ------------- |
| 28.01.2024 | First version |
