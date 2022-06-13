import requests
import pandas as pd
from bs4 import BeautifulSoup



def get_csv_url(url,date):

    results = requests.get(url)
    doc = BeautifulSoup(results.text, "html.parser")
    gfg = doc.find(lambda tag: tag.name == "td" and date in tag.text)
    link = gfg.parent.find("a").text
    csv_url = url+link
    return csv_url

def download_csv(url):
    r = requests.get(url)
    open("data.csv", 'wb').write(r.content)

def get_highest_temperature():
    df = pd.read_csv("data.csv")
    highest_temperature = df["HourlyDryBulbTemperature"].max()
    return highest_temperature
def main():
    url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'
    date = "2022-02-07 14:03"

    csv_download_url = get_csv_url(url,date)
    download_csv(csv_download_url)
    print(get_highest_temperature())
if __name__ == '__main__':
    main()
