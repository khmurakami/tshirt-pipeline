#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python Default Libraries
import os
import json

# Third Party Libraries
from google.cloud import storage

class GCPBucket():

    def __init__(self):

        self.bucket_client = storage.Client()

    def bucket_exists(self, bucket_name):
        """Check if a bucket exists with name
        Args:
            bucket_name (string): The name of the bucket you want to check
        Return:
            status (bool): True if the bucket exists. False if not
        """

        bucket = self.bucket_client.get_bucket(bucket_name)
        print(bucket)
        return bucket

    def create_bucket(self, bucket_name):

        # The name for the new bucket
        bucket_name = bucket_name

        if self.bucket_exists:
            # Creates the new bucket
            bucket = self.bucket_client.create_bucket(bucket_name)
            print('Bucket {} created.'.format(bucket.name))
        else:
            print("Bucket already exists")

    def upload_file(self, bucket_name, bucket_file_path, local_file_path):

        """Upload a file to a specified bucket
        Args:
            bucket_name (string): The name of the bucket
            bucket_file_path (string): The file location you want to upload the file to in the bucket
            local_file_path (string): The location of the file on your system that you want to upload
        Return:
            None
        """

        bucket = self.bucket_client.get_bucket(bucket_name)
        blob = bucket.blob(bucket_file_path)
        blob.upload_from_filename(local_file_path)
        print("uploaded file")

    def list_bucket_files(self, bucket_name, bucket_file_path):

        """List all of the files in a bucket by a specific path

        Args:
            bucket_name (string): Name of the bucket
            bucket_file_path (string): The folder(s) you want to list the contents of

        Return
            blobs (list of Strings) The contents of the bucket in a list

        """

        bucket = self.bucket_client.bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix='data/'))
        return blobs

    def create_public_url(self, bucket_name, bucket_path):

        """Create downloadable bucket url. Based on this: http(s)://storage.googleapis.com/[bucket]/[object]

        Args:
            bucket_name (string): Name of the bucket
            bucket_path (string): Name to the object you want to create a public url of

        """

        url = "https://storage.googleapis.com/{0}/{1}".format(bucket_name, bucket_path)
        return url
