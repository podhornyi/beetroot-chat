#!/bin/sh
set -xe

if [ -z $1 ]; then
    echo "Env should be passed"
    exit 1
fi

if [ -z $2 ]; then
    echo "Container image url is not defined"
    exit 1
fi

ENVIRONMENT=$1
CONTAINER_IMAGE_NAME=$2

echo "Building GIT-SYNC docker image"
docker build \
      -f ./deployment/Dockerfile \
      -t ${CONTAINER_IMAGE_NAME} \
      --build-arg ENVIRONMENT=$ENVIRONMENT .

exit 0