import requests, re, os, time
from bs4 import BeautifulSoup
from python_backend.download_file import download_file
from python_backend.constants import DOWNLOADED_FILES_FOLDER, LONG_STORAGE_FILES_FOLDER, CASE_COUNT_FILE, PYTHON_BACKEND_FOLDER

def downloaded_files_folder():
    return f"{PYTHON_BACKEND_FOLDER}/{DOWNLOADED_FILES_FOLDER}"

def long_storage_files_folder():
    return f"{PYTHON_BACKEND_FOLDER}/{LONG_STORAGE_FILES_FOLDER}"

def name_file(number):
    return f"{downloaded_files_folder()}/Case{number}.docx"

def case_count_file():
    return f"{long_storage_files_folder()}/{CASE_COUNT_FILE}"

def get_case_count():
    with open(case_count_file(), "r") as file:
        return int(file.read().strip())

def set_case_count(num_cases):
    with open(case_count_file(), "w") as file:
        file.write(str(num_cases))

def download_cases(download_delay=0, download_all_versions=False):
    names = []
    case_n = 0

    URL = "https://hsld.debatecoaches.org"

    def cook_soup(url):
        nonlocal download_delay
        time.sleep(download_delay)
        print(f"Cooking Soup for {url}")
        page = requests.get(url)
        return BeautifulSoup(page.content, "html.parser")

    soup = cook_soup(URL)

    try:
        os.makedirs(long_storage_files_folder())
    except FileExistsError:
        print(f"Skipping Creating Folder \"{long_storage_files_folder()}\" -- already exists")

    try:
        os.makedirs(downloaded_files_folder())
    except FileExistsError:
        print(f"Skipping Creating Folder \"{downloaded_files_folder()}\" -- already exists")

    div = soup.find("div", {"class": "Schools"})

    links = div.find_all("span", {"class": "wikilink"})

    anchors = [link.find("a") for link in links]

    hrefs = [anchor['href'] for anchor in anchors]

    hrefs = hrefs[:2] # was only using some for testing

    for href in hrefs:
        school_url = URL + href
        
        school_soup = cook_soup(school_url)

        school_table = school_soup.find("table")

        school_links = school_table.find_all("span", {"class": "wikilink"})

        school_anchors = [school_link.find("a") for school_link in school_links]

        school_hrefs = [school_anchor['href'] for school_anchor in school_anchors]

        for school_href in school_hrefs:
            case_url = URL + school_href

            case_soup = cook_soup(case_url)

            download_links = re.findall(r'https:\/\/hsld\.debatecoaches\.org\/download\/[^"]*', str(case_soup))

            if download_all_versions:
                for download_link in download_links:
                    fname = name_file(case_n)
                    time.sleep(download_delay)
                    download_file(fname, download_link)
                    names.append(fname)
                    case_n += 1
            elif len(download_links) > 0:
                fname = name_file(case_n)
                time.sleep(download_delay)
                download_file(fname, download_links[0])
                names.append(fname)
                case_n += 1
            

    set_case_count(case_n)
    return names

if __name__ == "__main__":
    download_cases()