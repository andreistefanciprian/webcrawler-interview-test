### Web Crawler 

Simple script that lists all internal and external links mentioned in all pages of a particular domain name (eg: https://some-website.com)

### Run script

```
# create python virtualenv and install dependencies
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt

# specify url to crawl inside the script (eg: url = 'https://some-website.com')

# run script
python web_crawler.py
```

### Script output

```
Foreign URLs: 499
Broken URLs: 0
Local URLs: 284

# the URLs will also be made available in a local json file
cat site_map.json
```

### Clean environment

```
# deactivate and delete python3 virtual environment
deactivate
rm -Rf .env
```