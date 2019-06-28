import threading
import time
import sys
import os

def parse_url(obj_url):
    """url: s3://bucket/object"""
    obj_url = obj_url[5:]#remove s3://
    return obj_url.split('/',1)

def build_url(bucket_name,object_name):
    return "s3://"+bucket_name+"/"+object_name

def list_objects(resource,bucket_name):
    try:
        bucket = resource.Bucket(bucket_name)
        return [key.key for key in bucket.objects.all()]
    except resource.meta.client.exceptions.NoSuchBucket:
        print("No such bucket:",bucket_name)
        return []

def delete_object(resource,obj_url):
    """delete object using s3 url"""
    bucket_name,key_name = parse_url(obj_url)
    obj = resource.Object(bucket_name,key_name)
    obj.delete()

def delete_bucket(resource,bucket_name):
    try:
        bucket = resource.Bucket(bucket_name)
        bucket.objects.all().delete()
    except resource.meta.client.exceptions.NoSuchBucket:
        pass

def create_bucket(resource,bucket_name):
    try:
        resource.create_bucket(Bucket=bucket_name)
    except resource.meta.client.exceptions.BucketAlreadyOwnedByYou:
        pass

def create_obj(resource,bucket_name,object_name,object_content):
    try:
        obj = resource.Object(bucket_name, object_name)
        obj.put(Body=object_content)
        return obj
    except resource.meta.client.exceptions.NoSuchBucket:
        print("No such bucket",bucket_name)
        return None

def put_object_blocks(resource,location,blocksize=10485760):
    """Uploads file to s3
        Read file from disk 1 blocksize at a time
       Locations is tuple of form: bucket name, file path, start offset, file length
    """
    url,local_path,offset,length = location
    bucket_name,object_name = parse_url(url)
    with open(local_path,"br") as f:
        f.seek(offset)
        if length < blocksize:
            content = f.read(length)
        else:
            content = bytearray()
            for i in range(blocksize,length,blocksize):
                content.extend(f.read(blocksize))
            i = len(content)
            if i < length:
                content.extend(f.read(length-i))
        obj = create_obj(resource,bucket_name, object_name, content)
        assert obj.content_length == length , "File upload incomplete!"
        del content

def put_object(resource,location):
    """Upload file to s3.
       loads file into bytearray
       Locations is tuple of form: bucket name, file path, start offset, file length
    """
    url,local_path,offset,length = location
    bucket_name,object_name = parse_url(url)
    with open(local_path,"br") as f:
        f.seek(offset)
        content = bytearray(length)
        f.readinto(content)
        obj = create_obj(resource,bucket_name, object_name, content)
        assert obj.content_length == length , "File upload incomplete!"
        del content
        return obj


def put_objects(resource,locations):
    """Bulk upload files"""
    threads = [threading.Thread(target = put_object, args = (resource,location)) for location in locations]
    for thread in threads:
        thread.start()
    return threads
