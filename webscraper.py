import requests
import time
import csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from config import config 

main_url = config.main_url
max_retries = config.max_retries
urls = config.urls
time_out = config.time_out
max_workers = config.max_workers
max_pages = config.max_pages

def create_csv_file_headers():
    with open('Webscraper.csv', 'a') as scraper:
        headers = ["URL's", "Title", "H1 Texts" , "H2 Texts", "HTML Size", "Response Code", "Download Time"]
        csvwriter = csv.writer(scraper)
        csvwriter.writerow(headers)

def download_page(url): 
    retries = 0
    while retries <= max_retries:
        try:
            response = requests.get(url, timeout= time_out)
            print("Page Downloaded")
            return response
        except:
            print("Error downloading the page !!!")
            retries += 1
            if retries == 1:
                print(f"Retrying for the {retries}st time ...")
            elif retries == 2:
                print(f"Retrying for the {retries}nd time ...")
            elif retries == 3:
                print(f"Retrying for the {retries}rd time ...")
            else:
                print(f"Retrying for the {retries}th time ...")
            print(f"Number if retries left : {max_retries - retries}")
    return None

def get_urls(url):
    response = download_page(url)
    if response:
        soup = BeautifulSoup(response.content, "html.parser")

        for link in soup.find_all('a', href = True):
            proper_link = str(link['href'])
            if proper_link.startswith(main_url) and proper_link not in urls and len(urls) <= max_pages:
                urls.append(proper_link)
                get_urls(proper_link)
        return urls
    
def scrape_data(url):
    start_time = time.time()
    response = download_page(url)
    end_time = time.time()
    response_code = response.status_code 

    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string.strip()
    h1_texts = [h1.get_text() for h1 in soup.find_all('h1')]
    h2_texts = [h2.get_text() for h2 in soup.find_all('h2')]
    html_size = len(response.content)
    download_time = end_time - start_time
    with open('Webscraper.csv', 'a', newline = '') as scraper:
        csvwriter = csv.writer(scraper)
        csvwriter.writerow([url, title, h1_texts, h2_texts, html_size, response_code, download_time])

def concurrency(urls):
    with ThreadPoolExecutor(max_workers = max_workers) as executor:
        for url in urls:
            executor.submit(scrape_data, url)
def main():
    create_csv_file_headers() 
    start = time.time() 
    urls = get_urls(main_url) 
    concurrency(urls)
    print(time.time()-start)

if __name__ == '__main__':
    main()