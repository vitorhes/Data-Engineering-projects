import boto3
from io import TextIOWrapper
from gzip import GzipFile
from io import StringIO


s3 = boto3.client('s3', region_name='eu-central-1') 

def download_stream_file(bucket,key,sequence):

    # get StreamingBody from botocore.response
    response = s3.get_object(Bucket=bucket, Key=key)
    # if gzipped
    gzipped = GzipFile(None, 'rb', fileobj=response['Body'])
    data = TextIOWrapper(gzipped)

    if sequence == 1:
        text_stream = StringIO()
        for line in data:
            text_stream.write(line)
        url = text_stream.getvalue().split('\n', 1)[0].rstrip()
        return url

    else:
        for line in data:
            print(line)

def main():

    BUCKET_NAME = "commoncrawl"
    FILE_KEY = "crawl-data/CC-MAIN-2022-05/wet.paths.gz"

    url = download_stream_file(BUCKET_NAME,FILE_KEY,1)
    download_stream_file(BUCKET_NAME,url,2)
 
if __name__ == '__main__':
    main()
