# taminatherme-crawler

## Setup

1. make sure, docker swarm is enabled (`docker info`)

   ![docker info](image.png)

1. if not: `docker swarm init`
1. write the secret for the DB into a docker secret: `echo -n "secret here" | docker secret create secure-key - `
1. you can also put the secret into a file and run `docker secret create secure-key - < my_key.txt`

TODO: did not use the key file...
