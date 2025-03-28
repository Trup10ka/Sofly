import requests
from bs4 import BeautifulSoup
from loguru import logger

BASE_URL = "https://www.asko-nabytek.cz"
OUTPUT_FILE = "links-gathered-asko.txt"
START_PAGE = 13
END_PAGE = 1

all_links = []

def fetch_links() -> int:
    logger.info(f"Start fetching links from {BASE_URL}")
    for page in range(START_PAGE, END_PAGE, -1):
        url = f"{BASE_URL}/pohovky?page={page}"
        print(f"Fetching page {page} - {url}...")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("div", { "class": "product" })

        for product in products:
            link_tag = product.find("a", { "class": "image" })
            if link_tag and "href" in link_tag.attrs:
                full_link = BASE_URL + link_tag["href"]
                all_links.append(full_link)

    # Save to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in all_links:
            f.write(link + "\n")

    print(f"Scraping completed. {len(all_links)} links saved to {OUTPUT_FILE}.")

    return len(all_links)

def asko_gather_links() -> int:
    return fetch_links()