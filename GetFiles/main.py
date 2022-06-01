
import requests
import os
import zipfile
import logging
import aiohttp
import asyncio
import re
import aiofiles

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
logging.basicConfig(filename = 'files.log', level = logging.INFO, 
                    format = "%(asctime)s:%(levelname)s:%(message)s")

download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

DIRECTORY = "downloads"
PATH = os.path.join(os.getcwd(), DIRECTORY)

async def get_files(url):
    #sema = asyncio.BoundedSemaphore(5)
    if url.find('/'):
        filename = url.rsplit('/', 1)[1]
    logging.info(f"Downloading file: {filename}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
               assert response.status == 200
               result = await response.read()
        async with aiofiles.open(os.path.join(PATH, filename), "wb") as outfile:

            outfile.write(result)
 




def create_filenames_dic(urls):
        urls_dict = {}
        for url in urls:
            if url.find('/'):
                filename = url.rsplit('/', 1)[1]
            urls_dict[filename] = url
        return urls_dict
            


def create_dir(path: str) -> None:
    """"
    Create the 'downloads' folder in the current directory
    """
    if not os.path.exists(path):
        os.mkdir(path)
        logging.info('Downloads directory created')
    else:
        logging.info('Downloads directory already exist')


def download_files(url: str, file_path: str, filename: str) -> None:
    try:
        r = requests.get(url, allow_redirects=True)
        open(file_path, 'wb').write(r.content)
        logging.info(f"Successfully downloaded: {filename}")

    except Exception as e:
         logging.error(f'Error when downloading the file: {e}')

  
def unzip_files(file_path: str, destination_path:str, filename:str) -> None:
    try:
        with zipfile.ZipFile(file_path,"r") as zip_ref:
            zip_ref.extractall(destination_path)
            logging.info(f"Successfully extracted: {filename}")
    except Exception as e:
        logging.error(f'Error when unziping: {e}')
       
def deleting_zip_files(file_path: str, filename:str) -> None:

    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f"Successfully deleted the file: {filename}")
        

def assert_url_exists(url: str) -> bool:
    try:
        r = requests.head(url)
        return r.status_code == requests.codes.ok
    except:
        return False
def main():

#     DIRECTORY = "downloads"
#     path = os.path.join(os.getcwd(), DIRECTORY)

#     create_dir(path)
    
#     for url in download_uris:
#         if url.find('/'):
#             filename = url.rsplit('/', 1)[1]
#         file_path = os.path.join(path, filename)
#         if assert_url_exists(url):
#                 download_files(url, file_path, filename)
#                 unzip_files(file_path,path, filename)
#                 deleting_zip_files(file_path, filename)
#         else:
#             logging.warning(f"The URL is invalid:{url}. Skipping to the next file") 
    create_dir(PATH)
    print("-----------Downloading files, please wait ---------")
    logging.info(f"Downloading files")
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(get_files(url)) for url in download_uris]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close() 
    logging.info(f"Loop closed. Finished")
    print("All files have been downloaded. Program finished")
if __name__ == '__main__':
    main()
