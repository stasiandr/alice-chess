#!/usr/bin/env bash

docker stop app
docker build -t app ./app
docker run -dp 5000:5000 --name app app

docker stop nginx
docker build -t nginx ./nginx
docker run -dp 5000:5000 --name nginx nginx
