import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging


def get_csv_url(url: str,date: str) -> str:
    """
    Get an url and find a specific date in the <td> tags.
    Then, return an url to download the csv file related to that date

    """
    try:
        results = requests.get(url)
        assert results.status_code == 200, f'Assertion error. Error while requesting url'
        logging.info(f"Request successfully fetched. status: {results.status_code}")
    except Exception as e:
        logging.error(e)

    doc = BeautifulSoup(results.text, "html.parser")
    soup = doc.find(lambda tag: tag.name == "td" and date in tag.text)
    link = soup.parent.find("a").text
    csv_url = url+link

    return csv_url

def download_csv(url:str) -> None:
    try:
        r = requests.get(url)
        assert r.status_code == 200, f'Assertion error. Error while requesting CSV file'
    except Exception as e:
        logging.error(e)
    
    open("data.csv", 'wb').write(r.content)
    

def get_highest_temperature()-> str:
    """
    Transform a csv file to a pandas dataframe, then return the highest temperature
    """
    try:
        df = pd.read_csv("data.csv")
        highest_temperature = df["HourlyDryBulbTemperature"].max()
        logging.info(f"CSV file transformed to dataframe and temperature fetched.")
    except Exception as e:
        logging.error(f'Some error occured while transforming file to dataframe: {e}')

    return highest_temperature

def main():

    logging.basicConfig(filename = 'files.log', level = logging.INFO, 
                format = "%(asctime)s:%(levelname)s:%(message)s")

    url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'
    date = "2022-02-07 14:03"

    csv_download_url = get_csv_url(url,date)
    download_csv(csv_download_url)

    highest_temperature = get_highest_temperature()
    print(highest_temperature)

if __name__ == '__main__':
    main()
