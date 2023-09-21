class WebScraperConfig:
    def __init__(self):
        self.main_url = 'https://www.dbizsolution.com/'
        self.max_retries = 3
        self.urls = []
        self.time_out = 5
        self.max_workers = 10
        self.max_pages = 20

config = WebScraperConfig()
