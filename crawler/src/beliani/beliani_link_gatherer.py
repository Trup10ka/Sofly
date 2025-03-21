from bs4 import BeautifulSoup

def beliani_gather_links() -> int:

    path_to_html = "input/pohovky_beliani.htm"
    # Load the HTML file
    with open(path_to_html, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")


    # Extract links
    links = []
    for product in soup.find_all("div", class_="product-teaser"):
        a_tag = product.find("a", class_="itemBox")
        if a_tag and a_tag.get("href"):
            links.append(a_tag["href"])

    # Save to file
    with open("links-gathered-beliani.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(links))

    print(f"Extracted {len(links)} links and saved to links-gathered.txt.")

    return len(links)
