#!/bin/bash

S3_ENDPOINT=http://minio:9000
S3_KEY=minio
S3_SECRET=miniosecretkey
NETWORK='composetest_default'
TEST_FILE="/tmp/big-file"
TEST_CMD='pytest .'
#TEST_CMD='python test_benchmark.py'
IMAGE='hackathon/python'


ENV="-e S3_ENDPOINT=$S3_ENDPOINT -e S3_KEY=$S3_KEY -e S3_SECRET=$S3_SECRET -e S3_FILE=$TEST_FILE"
docker build . --tag $IMAGE --quiet
docker run $ENV -v /tmp:/tmp --rm --network=$NETWORK $IMAGE $TEST_CMD

