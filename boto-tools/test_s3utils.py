import pytest
import boto3
import boto3.session
import os
from s3utils import *

bucket_name="test-bucket"

def test_create_bucket(resource):
    delete_bucket(resource,bucket_name)
    create_bucket(resource,bucket_name)


def test_list_objects(resource):
    out = list_objects(resource,bucket_name)
    assert out == []

    create_obj(resource,bucket_name,"test_str","test_str contents");
    out = list_objects(resource,bucket_name)
    assert len(out) == 1 and out[0] == "test_str"

    delete_object(resource,build_url(bucket_name,"test_str"))
    out = list_objects(resource,bucket_name)
    assert out == []

def test_put_objects(resource):
    test_file=os.environ.get("S3_FILE")
    names = ["test"+str(x) for x in range(3)]
    url = [build_url(bucket_name,object_name)for object_name in names]
    locations = [(url[0],test_file,0,2048000),
            (url[1],test_file,0, 1024000 ),
            (url[2],test_file,1024000, 1024000)]
    threads = put_objects(resource, locations)
    for t in threads:
        t.join()
    out = list_objects(resource,bucket_name)
    print(locations)
    assert all(x in out for x in names)

def test_clean_up(resource):
    delete_bucket(resource,bucket_name)


