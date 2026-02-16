#!/bin/sh
set -e

export AWS_ACCESS_KEY_ID=any
export AWS_SECRET_ACCESS_KEY=any
export AWS_DEFAULT_REGION=us-east-1

echo "Waiting for SeaweedFS S3 to be ready..."

until aws --endpoint-url=http://seaweed-s3:8333 s3 ls >/dev/null 2>&1; do
  echo "waiting..."
  sleep 2
done

echo "Seaweed S3 is ready!"

aws --endpoint-url=http://seaweed-s3:8333 s3 mb s3://bronze || true
aws --endpoint-url=http://seaweed-s3:8333 s3 mb s3://silver || true
aws --endpoint-url=http://seaweed-s3:8333 s3 mb s3://gold   || true
aws --endpoint-url=http://seaweed-s3:8333 s3 mb s3://mage   || true

aws --endpoint-url=http://seaweed-s3:8333 s3 ls
