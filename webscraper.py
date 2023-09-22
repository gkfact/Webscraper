import time
import csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from config import config
from download import Downloader

class WebScraper:
    def __init__(self):
        self.create_csv_file_headers()

    def create_csv_file_headers(self):
        with open('Webscraper.csv', 'a') as scraper:
            headers = ["URL's", "Title", "H1 Texts", "H2 Texts", "HTML Size", "Response Code", "Download Time"]
            csvwriter = csv.writer(scraper)
            csvwriter.writerow(headers)

    def get_urls(self, url):
        response = Downloader.download_page(url)
        if response:
            soup = BeautifulSoup(response.content, "html.parser")

            for link in soup.find_all('a', href=True):
                proper_link = str(link['href'])
                if proper_link.startswith(config.main_url) and proper_link not in config.urls and len(config.urls) <= config.max_pages:
                    config.urls.append(proper_link)
                    self.get_urls(proper_link)
            return config.urls

    def scrape_data(self, url):
        start_time = time.time()
        response = Downloader.download_page(url)
        end_time = time.time()
        response_code = response.status_code

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip()
        h1_texts = [h1.get_text() for h1 in soup.find_all('h1')]
        h2_texts = [h2.get_text() for h2 in soup.find_all('h2')]
        html_size = len(response.content)
        download_time = end_time - start_time
        with open('Webscraper.csv', 'a', newline='') as scraper:
            csvwriter = csv.writer(scraper)
            csvwriter.writerow([url, title, h1_texts, h2_texts, html_size, response_code, download_time])

    def concurrency(self):
        with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
            for url in config.urls:
                executor.submit(self.scrape_data, url)

    def run(self):
        start = time.time()
        config.urls = self.get_urls(config.main_url)
        self.concurrency()
        print(time.time() - start)
