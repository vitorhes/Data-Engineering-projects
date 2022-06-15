from fileinput import filename
import boto3
import botocore
from botocore.client import Config

import gzip



s3 = boto3.client('s3', region_name='eu-central-1') 
s3.meta.events.register('choose-signer.s3.*', botocore.handlers.disable_signing)  

def lista(bucket_name):
    objects = s3.list_objects(Bucket=bucket_name)
    for item in objects["Contents"]:
        print (item)
def download_from_bucket(bucket_name: str, file_key: str):

    s3_response_object = s3.get_object(Bucket= bucket_name, Key= file_key)
    object_content = s3_response_object['Body'].read()
    return object_content

def decompress_file(object,filename):

    with open(filename, 'wb') as outfile:
        outfile.write(gzip.decompress(object))

def get_url(filename):

    first_line=open(filename).readline().rstrip()

    return first_line

def main():

    BUCKET_NAME = "commoncrawl"
    FILE_KEY = "crawl-data/CC-MAIN-2022-05/wet.paths.gz"
    filename = "outfile.txt"
    lista(BUCKET_NAME)
    object = download_from_bucket(BUCKET_NAME,FILE_KEY)
    decompress_file(object,filename)
    url = get_url(filename)
    print(url)
    #object2 = download_from_bucket(BUCKET_NAME,url)
    #decompress_file(object2,"finaloutput.txt")

if __name__ == '__main__':
    main()
