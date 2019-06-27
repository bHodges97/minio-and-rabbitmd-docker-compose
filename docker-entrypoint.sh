#!/bin/sh

set -eu

mkdir -p /root/.mc
cat > /root/.mc/config.json <<EOF
{
  "version": "9",
  "hosts": {
    "minio": {
      "url": "http://minio:9000",
      "accessKey": "${MINIO_ACCESS_KEY}",
      "secretKey": "${MINIO_SECRET_KEY}",
      "api": "s3v4",
      "lookup": "auto"
    }
  }
}
EOF

. /usr/bin/docker-entrypoint-minio.sh
