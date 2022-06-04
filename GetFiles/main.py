import os
import zipfile
import logging
import aiohttp
import asyncio
import aiofiles
import platform




urls_list = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
]



async def get_files(url:str, path: str) -> None:

    if url.find('/'):
        filename = url.rsplit('/', 1)[1]
    logging.info(f"Downloading file: {filename}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
               assert response.status == 200
               result = await response.read()
        async with aiofiles.open(os.path.join(path, filename), "wb") as outfile:

            await outfile.write(result)


def create_dir(path: str) -> None: 

    if not os.path.exists(path):
        os.mkdir(path)
        logging.info('Downloads directory created')
    else:
        logging.info('Downloads directory already exist')

def get_zipfiles_filenames(path: str) -> list:

    zipfiles_filenames  = []
    for filename in os.listdir(path):
    
        if filename.endswith(".zip"): 
            file_path = os.path.join(path, filename)
            zipfiles_filenames.append(file_path)

    return zipfiles_filenames

def unzip_files(zipfile_filenames_list: list, path: str) -> None:

    for zipfile_filename in zipfile_filenames_list:

        try:
            with zipfile.ZipFile(zipfile_filename,"r") as zip_ref:

                zip_ref.extractall(path)
                logging.info(f"Successfully extracted: {zipfile_filename}")

        except Exception as e:
            logging.error(f'Error when unziping or deleting file {zipfile_filename}. Error: {e}')

def delete_zip_files(zipfile_filenames_list: list) -> None:

     for zipfile_filename in zipfile_filenames_list:

        try:

            os.remove(zipfile_filename)
            logging.info(f"Successfully deleted the file: {zipfile_filename}")

        except Exception as e:
            logging.error(f'Error when deleting file {zipfile_filename}. Error: {e}')

def main():
    
    logging.basicConfig(filename = 'files.log', level = logging.INFO, 
                    format = "%(asctime)s:%(levelname)s:%(message)s")

    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    DIRECTORY = "downloads"
    PATH = os.path.join(os.getcwd(), DIRECTORY)

    create_dir(PATH)
    print("----------- Downloading files, please wait ---------")

    
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(get_files(url,PATH)) for url in urls_list]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close() 

    logging.info(f"Loop closed. Extracting and then deleting zip files")

    zipfile_filenames_list = get_zipfiles_filenames(PATH)
    unzip_files(zipfile_filenames_list,PATH)
    delete_zip_files(zipfile_filenames_list)
    
    print("All files have been downloaded and extracted.")

if __name__ == '__main__':
    main()
