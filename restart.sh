#!/usr/bin/env bash

docker network create mynet

docker stop app
docker rm app
docker build -t app ./app
docker run -dp 5000:5000 --name app --net mynet app

docker stop nginx
docker rm nginx
docker build -t nginx ./nginx
docker run -d -p 80:80 -p 443:443 --name nginx --net mynet -v /etc/letsencrypt:/etc/letsencrypt nginx
