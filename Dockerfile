FROM minio/mc AS client
FROM minio/minio
COPY --from=client /usr/bin/mc /usr/bin/mc
COPY amqpconfig /data/.minio.sys/config/config.json
COPY addevent.sh /tmp/addevent.sh
#CMD ["/tmp/addevent.sh"]
#COPY notifications.xml /data/.minio.sys/buckets/test/notification.xml

