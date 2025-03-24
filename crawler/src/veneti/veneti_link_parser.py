import re

from requests import RequestException

from src.util import get_soup_parser, init_data_map, finalize_parsed_dict, VENETI_DESCRIPTION_KEYS, map_key

def set_hardwood_and_steel_to_zero_if_not_detected(data_dict: dict):
    if data_dict["contains_metal"] == -1:
        data_dict["contains_metal"] = 0

    if data_dict["contains_hardwood"] == -1:
        data_dict["contains_hardwood"] = 0

def check_if_contains_hardwood_or_metal(data_dict, soup):
    description_div = soup.find('div', class_='product-description')
    list_of_descriptions = description_div.find_all('ul')[1].find_all('li')

    for description in list_of_descriptions:
        if any(word in description.text.lower() for word in ["kovové", "ocel", "ocelové", "železo", "železné"]):
            data_dict["contains_metal"] = 1

        elif any(word in description.text.lower() for word in ["dřevo", "dřevěné", "masiv"]):
            data_dict["contains_hardwood"] = 1

    set_hardwood_and_steel_to_zero_if_not_detected(data_dict)

def process_value(data_dict, value, key):
    mapped_key = map_key(key.lower().strip())
    value = value.text.strip().lower()

    if mapped_key == "cover_material":
        if value in ["látka", "textil"]:
            value = "fabric"
        elif value in ["kůže", "koženka"]:
            value = "leather"

    data_dict[mapped_key] = value

def parse_veneti_price(price_text: str) -> float:
    cleaned_price_text = re.sub(r'[^\d,.-]', '', price_text)
    return float(cleaned_price_text.replace(",", "."))

def parse_veneti_link(page_link: str) -> dict:
    try:
        soup = get_soup_parser(page_link)

        main_price = soup.find('span', class_='current-price-value')
        price_text = main_price.text if main_price else None
        if price_text is None:
            raise Exception("Price not found")

        data_dict = init_data_map()
        data_dict["price"] = parse_veneti_price(price_text)

        keys = soup.find_all('dt', class_='name')
        values = soup.find_all('dd', class_='value')

        for index, key in enumerate(keys):
            if key.text.lower().strip() not in VENETI_DESCRIPTION_KEYS:
                continue
            process_value(data_dict, values[index], key.text)

        check_if_contains_hardwood_or_metal(data_dict, soup)

        return data_dict

    except RequestException as e:
        print(f"Failed to fetch {page_link}: {e}")
        return {}

def parse_veneti_links() -> int:
    total_parsed_links = 0
    all_sofas_parsed_links = []
    with open("links-gathered-veneti.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

        for link in links:
            print(f"Parsing link: {link}")
            parsed_data = parse_veneti_link(link.strip())
            if len(parsed_data) == 0:
                continue

            if not finalize_parsed_dict(all_sofas_parsed_links, parsed_data):
                print(f"Failed to parse link: {link}")
            else:
                total_parsed_links += 1
    return total_parsed_links