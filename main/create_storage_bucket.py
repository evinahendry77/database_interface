#!/bin/python3
# Program name: create_storage_bucket.py
# Creator: Evin Hendry
# Date created: December 7th, 2020
# Purpose: Creates an S3 bucket.

from __future__ import print_function
import boto3
import json
import decimal

s3 = boto3.client('s3')

# Place your bucket's fully qualified domain name here.

s3.create_bucket(Bucket=YOUR_BUCKET_HERE)
