from bs4 import BeautifulSoup
import os

def veneti_gather_links() -> int:
    # Define file paths
    input_file = "input/pohovky_veneti.html"
    output_file = "links-gathered-veneti.txt"

    # Read the HTML file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} does not exist.")
    if os.path.getsize(input_file) == 0:
        raise ValueError(f"Input file {input_file} is empty.")
    with open(input_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find all divs with class 'ajax_block_product'
    products = soup.find_all("div", class_="ajax_block_product")

    # Extract href links from <a> with class 'product-thumbnail'
    links = [a["href"] for div in products if (a := div.find("a", class_="product-thumbnail")) and "href" in a.attrs]

    # Save links to a file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(links))

    print(f"Extracted {len(links)} links and saved to {output_file}")

    return len(links)
