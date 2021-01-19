#!/usr/bin/env bash

docker stop app
docker rm app
docker build -t app ./app
docker run -dp 5000:5000 --name app app

docker stop nginx
docker rm nginx
docker build -t nginx ./nginx
docker run -dp 80:80 --name nginx -v /var/www/cert:/var/www/cert nginx
