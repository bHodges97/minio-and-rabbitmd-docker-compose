# A MinIO set-up with AMQP notifications

This project sets up a [MinIO](https://min.io/) instance with [Docker
Compose](https://docs.docker.com/compose/), which sends AMQP
notifications to a [RabbitMQ](https://www.rabbitmq.com/) instance.


## Set up

The script [bootstrap](./bootstrap) initializes from scratch the MinIO
and RabbitMQ instances:

```
$ ./bootstrap
Destroying Docker Compose environment ...
Stopping minio-and-rabbitmd-docker-compose_minio_1    ...
Stopping minio-and-rabbitmd-docker-compose_rabbitmq_1 ...
Stopping minio-and-rabbitmd-docker-compose_minio_1    ... done
Stopping minio-and-rabbitmd-docker-compose_rabbitmq_1 ... done
Going to remove minio-and-rabbitmd-docker-compose_minio_1, minio-and-rabbitmd-docker-compose_rabbitmq_1
Removing minio-and-rabbitmd-docker-compose_minio_1    ...
Removing minio-and-rabbitmd-docker-compose_rabbitmq_1 ...
Removing minio-and-rabbitmd-docker-compose_rabbitmq_1 ... done
Removing minio-and-rabbitmd-docker-compose_minio_1    ... done
Building container image ...
sha256:606881c0b20abaf557eadf233030a7d62f8aeb689fdc5ee66b659a498e551845
Starting Docker Compose environment ...
Creating minio-and-rabbitmd-docker-compose_rabbitmq_1 ...
Creating minio-and-rabbitmd-docker-compose_rabbitmq_1 ... done
Creating minio-and-rabbitmd-docker-compose_minio_1    ...
Creating minio-and-rabbitmd-docker-compose_minio_1    ... done
Waiting for RabbitMQ ...
Waiting for MinIO ...
Creating RabbitMQ exchange ...
Creating RabbitMQ queue ...
Binding RabbitMQ queue to exchange ...
Configuring MinIO AMQP notifications ..
Setting new MinIO configuration file has been successful.
Please restart your server with `mc admin service restart`.

Restart command successfully sent to `minio`.
Restarted `minio` successfully.
Creating MinIO bucket ...
Bucket created successfully `minio/sample-bucket`.
Configuring MinIO bucket notifications ...
Successfully added arn:minio:sqs::1:amqp
$
```


## Accessing the MinIO instance

The MinIO UI is available at http://localhost:9000, with the following
credentials:

* Access key: `minio`
* Secret key: `miniosecretkey`


## Accessing the RabbitMQ instance

The RabbitMQ UI is available at http://localhost:15672, with the
following credentials:

* Username: `guest`
* Password: `guest`


## AMQP notifications

The boostrap script creates an S3 bucket called `sample-bucket`. It
also created an AMQP topic exchange called `minio`, bound to the AMQP
queue `sample-queue` with routing key `#`.

S3 events on `sample-bucket` are propagated to the AMQP queue
`sample-queue`.

## BOTO3 Tests and Benchmark
Place a 100 MB test file in the boto-tools/data/ directory and then run run_tests.sh from within the boto-tools directory.
Test results are stored in boto-tools/data.
```
$ cd boto-tools/data
$ dd if=/dev/zero of=bigfile.txt count=1 bs=100M
$ cd ..
$ ./run_test.sh
```
