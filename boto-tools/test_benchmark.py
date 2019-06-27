import time
import boto3
import boto3.session
import os
from s3utils import *

def test_time(resource):
    bucket_name="test-benchmark"
    test_file=os.environ.get("S3_FILE")
    create_bucket(resource,bucket_name)

    urls = [build_url(bucket_name,"test"+str(i)) for i in range(20)]
    locations = [(urls[1],test_file,0,104857600)]
    t = time.time()
    threads = put_objects(resource, locations)
    for thread in threads:
        thread.join()
    print("1 * 100Mb:",time.time()-t)

    locations = [(urls[2],test_file,0,52428800),
                (urls[3],test_file,52428800,52428800)]
    t = time.time()
    threads = put_objects(resource, locations)
    for thread in threads:
        thread.join()
    print("2 * 50Mb:",time.time()-t)

    locations = [(urls[4],test_file,0,26214400),
            (urls[5],test_file,26214400,26214400),
            (urls[6],test_file,52428800,26214400),
            (urls[7],test_file,78643200,26214400)]
    t = time.time()
    threads = put_objects(resource, locations)
    for thread in threads:
        thread.join()
    print("4 * 25Mb:",time.time()-t)

    delete_bucket(resource,bucket_name)
