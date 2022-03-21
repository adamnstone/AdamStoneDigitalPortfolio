import urllib.request
import shutil

def download_file(destination, url):
    print(f"Downloading {url}")
    with urllib.request.urlopen(url) as response, open(destination, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return destination