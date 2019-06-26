FROM minio/mc:RELEASE.2019-06-19T22-39-53Z AS client

FROM minio/minio:RELEASE.2019-06-19T18-24-42Z

COPY --from=client /usr/bin/mc /usr/bin/mc

RUN set -eux \
	&& apk add bash jq

RUN set -eux \
	&& wget -O /usr/bin/wait-for-it \
	https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
	&& chmod 0755 /usr/bin/wait-for-it

RUN set -eux \
	&& cp /usr/bin/docker-entrypoint.sh /usr/bin/docker-entrypoint-minio.sh

COPY docker-entrypoint.sh /usr/bin/
RUN set -eux \
	&& chmod 0755 /usr/bin/docker-entrypoint.sh

COPY setup-amqp-notifications /usr/bin/
RUN set -eux \
	&& chmod 0755 /usr/bin/setup-amqp-notifications
