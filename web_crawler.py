import requests
from bs4 import BeautifulSoup
import json


class WebCrawler:
    """
    Simple Web Crawler.
    Visits all pages within the target domain.
    Doesn't follow the links to external sites.
    Outputs in json file links to internal URLs, external URLs and broken URLs.
    """

    def __init__(self, url):
        self.url = url
        self.site_map = {}
        self.unprocessed_urls = set()
        self.local_urls = set()
        self.foreign_urls = set()
        self.broken_urls = set()

    def parse_url(self):

        """
        Web crawler function.
        Parses all local links belonging to target domain.
        """

        self.unprocessed_urls.add(self.url)

        while len(self.unprocessed_urls):
            # get url to be parsed from the new_urls set
            new_url = self.unprocessed_urls.pop()

            if new_url not in self.local_urls:
                try:
                    response = requests.get(new_url)
                except:
                    self.broken_urls.add(new_url)
                    print(f'URL BROKEN: {new_url}')
                else:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # for each URL found in the url's page
                    for found_url in soup.find_all('a', href=True):
                        found_url = found_url['href']
                        if url in found_url:
                            # add url to the set of new unprocessed local urls
                            self.unprocessed_urls.add(found_url)
                            print(f'URL TO BE PARSED: {found_url}')
                        else:
                            # add url to the set of foreign urls
                            self.foreign_urls.add(found_url)
                            print(f'URL FOREIGN: {found_url}')
                    # add it to the set of local parsed urls
                    self.local_urls.add(new_url)
                    print(f'URL PARSED: {new_url}')
            else:
                print(f'URL ALREADY PARSED: {new_url}')

    def display_results(self):
        """Display results."""

        print(f'Left to be parsed URLs: {len(self.unprocessed_urls)}')
        print(f'Foreign URLs: {len(self.foreign_urls)}')
        print(f'Broken URLs: {len(self.broken_urls)}')
        print(f'Local URLs: {len(self.local_urls)}')

    def create_site_map_json(self, json_file_name):
        """
        Output site map to json file!
        return: dict
        """

        # create site map dictionary based on found urls
        self.site_map['LOCAL_PARSED_URLS'] = list(self.local_urls)
        self.site_map['FOREIGN_URLS'] = list(self.foreign_urls)
        self.site_map['BROKEN_URLS'] = list(self.broken_urls)
        # write site map dictionary to json file
        with open(json_file_name, "w") as write_file:
            json.dump(self.site_map, write_file)
            print(f'\nSite map for {self.url} made available locally at {json_file_name}.')

        return dict


if __name__ == "__main__":

    # specify url to crawl
    url = 'https://wiprodigital.com'

    # parse url
    crawl = WebCrawler(url)
    crawl.parse_url()

    # print results
    crawl.display_results()

    # create json file with parsed urls
    crawl.create_site_map_json("site_map.json")
