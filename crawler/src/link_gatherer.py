import requests
from bs4 import BeautifulSoup

def fetch_links(page_url, output_file_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(page_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    product_divs = soup.find_all("div", class_="product-teaser")

    links = []
    for div in product_divs:
        a_tag = div.find("a", class_="itemBox")
        if a_tag and "href" in a_tag.attrs:
            links.append(a_tag["href"])

    with open(output_file_path, "w", encoding="utf-8") as file:
        for link in links:
            file.write(link + "\n")

    print(f"Successfully saved {len(links)} links to {output_file_path}")


def gather_links():
    url = "https://www.beliani.cz/nabytek-do-obyvaku/pohovky/vsechny+produkty/"
    output_file = "links-gathered.txt"
    fetch_links(url, output_file)
