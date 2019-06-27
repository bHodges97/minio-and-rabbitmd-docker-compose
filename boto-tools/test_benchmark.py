import time
import boto3
import boto3.session
import os
import pytest
from s3utils import *

test_file=os.environ.get("S3_FILE")
bucket_name="test-benchmark"
urls = [build_url(bucket_name,"test"+str(i)) for i in range(20)]


def test_upload1(benchmark,resource):
    locations = [(urls[1],test_file,0,104857600)]
    create_bucket(resource,bucket_name)
    benchmark(upload,resource,locations)

def test_upload2(benchmark,resource):
    locations = [(urls[2],test_file,0,52428800),
                (urls[3],test_file,52428800,52428800)]
    benchmark(upload,resource,locations)

def test_upload3(benchmark,resource):
    locations = [(urls[4],test_file,0,26214400),
            (urls[5],test_file,26214400,26214400),
            (urls[6],test_file,52428800,26214400),
            (urls[7],test_file,78643200,26214400)]
    benchmark(upload,resource,locations)
    delete_bucket(resource,bucket_name)

def upload(resource,locations):
    threads = put_objects(resource, locations)
    for thread in threads:
        thread.join()
