#!/usr/bin/env bash

docker stop app

docker build -t app ./app

docker run -dp 5000:5000 --name app app