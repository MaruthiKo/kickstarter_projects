from datetime import datetime
from urllib.request import urlretrieve
from zipfile import ZipFile

def datetime_converter(integer):
    # Given integer representing a Unix timestamp
    timestamp = integer

    # Convert Unix timestamp to a datetime object
    dt_object = datetime.utcfromtimestamp(timestamp)

    # Format the datetime object as a string (adjust format as needed)
    formatted_datetime = dt_object.strftime('%Y-%m-%d')
    return formatted_datetime

def day_extractor(x):
    day = x.split(" ")[0]
    return int(day)

def downloader():
    url = "https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2023-10-12T03_20_02_365Z.zip"
    path = "../data/csv_files/raw_data.zip"
    urlretrieve(url, path)
    with ZipFile(path, 'r') as zipObj:
        zipObj.extractall("../data/csv_files/")
