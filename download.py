import requests
import time
from config import config

class Downloader:
    def download_page(url, retries=0):
        if retries <= config.max_retries:
            try:
                response = requests.get(url, timeout=config.time_out)
                print("Page Downloaded")
                return response
            except:
                print("Error downloading the page !!!")
                retries += 1
                print(f"Retrying for the {retries}{'st' if retries == 1 else 'nd' if retries == 2 else 'rd' if retries == 3 else 'th'} time ...")
                print(f"Number of retries left: {config.max_retries - retries}")
                return Downloader.download_page(url, retries)
        return None
