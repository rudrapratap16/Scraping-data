from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from datetime import date
import os

output_dir = './weekly_data'
os.makedirs(output_dir, exist_ok=True)

try:
    # Get the Webpage
    url = "https://inc42.com/tag/funding-galore/"
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')

    # Get latest link
    new_soup = soup.find("main", {"id": "main"})
    new_links = new_soup.find_all('a')
    link = new_links[0].get("href")

    # Getting the webpage
    req = Request(
        url=link, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()

    # Filtering the content
    df_tables = pd.read_html(webpage)
    column = list(df_tables[0].iloc[0])
    df_tables[0].columns = column
    df_tables = df_tables[0].shift(-1)
    df_tables = df_tables.shift(2)
    df_tables.dropna(inplace=True)

    name = [l for l in link.split('/') if l != '']
    name_csv = f"Till-{str(date.today())} - {name[-1]}"

    path = f'./weekly_data/{name_csv}.csv'

    df_tables.to_csv(path)
except Exception as e:
    print(f"An Error Occured : {e}")
    raise