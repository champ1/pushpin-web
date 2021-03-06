#!/bin/sh

# for use during local development to kill and redeploy everything, then make sure it deployed successfully

sudo docker build -t dakotanelson/pushpin .

sudo docker stop pushpin-postgres
sudo docker stop pushpin

sudo docker rm pushpin-postgres
sudo docker rm pushpin

sudo docker run --name pushpin-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=pushpin -d postgres
sleep 5
sudo docker run --name pushpin -p 8000:8000 -p 8001:8001 --link pushpin-postgres:postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_PORT=5432 -e DJANGO_PASSWORD=test -e DEBUG=True -d dakotanelson/pushpin

sleep 20

sudo docker logs pushpin
