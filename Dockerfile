FROM minio/mc:RELEASE.2019-06-19T22-39-53Z AS client

FROM minio/minio:RELEASE.2019-06-19T18-24-42Z
COPY --from=client /usr/bin/mc /usr/bin/mc
COPY amqpconfig /data/.minio.sys/config/config.json
COPY addevent.sh /tmp/addevent.sh
#CMD ["/tmp/addevent.sh"]
#COPY notifications.xml /data/.minio.sys/buckets/test/notification.xml

