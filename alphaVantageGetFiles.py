import csv
import requests
from config import API_KEY

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
CSV_URL = f'https://alphavantage.co/query?function=LISTING_STATUS&date=2013-01-01&&apikey={API_KEY}'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)