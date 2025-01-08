#!/bin/bash

echo "This Shell Script is Enter Mongo Docker"

# docker ps 결과 중 "haru-stock-mongo-master"를 grep, awk로 ID 추출
dockerId=$(docker ps | grep haru-stock-mongo-master | awk '{print $1}')

docker exec -it $dockerId bash