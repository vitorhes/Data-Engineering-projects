import boto3
from io import TextIOWrapper, StringIO
from gzip import GzipFile
import logging

logging.basicConfig(filename = 'files.log', level = logging.INFO, 
                format = "%(asctime)s:%(levelname)s:%(message)s")

def download_stream_file(bucket: str, key: str, s3) -> str:
    """
    fetch a gz file and stream it from a public S3 bucket
    """

    try:
    # get StreamingBody from botocore.response

        response = s3.get_object(Bucket=bucket, Key=key)
        object = GzipFile(None, 'rb', fileobj=response['Body'])
        data = TextIOWrapper(object)

    except Exception as e:
        logging.error(e)

    return data

def main():

    s3_conn = boto3.client('s3', region_name='eu-central-1') 
    BUCKET_NAME = "commoncrawl"
    FILE_KEY = "crawl-data/CC-MAIN-2022-05/wet.paths.gz"

    #download the file in memory to fetch the url located in the first line of the file
    text_stream = StringIO()

    for line in download_stream_file(BUCKET_NAME,FILE_KEY,s3_conn):
        text_stream.write(line)
    url = text_stream.getvalue().split('\n', 1)[0].rstrip()
    logging.info(f"URL fetched: {url}")

    #use the url fetched above to download the second file, then stream and print it line by line
    for line in download_stream_file(BUCKET_NAME,url,s3_conn):
        print(line)
    logging.info(f"Finished printing the file")

 
if __name__ == '__main__':
    main()
