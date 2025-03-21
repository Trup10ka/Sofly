import requests
from bs4 import BeautifulSoup

from src.util import init_data_map, finalize_parsed_dict, append_parsed_data, get_soup_parser, BELIANI_DESCRIPTION_KEYS


def map_material(material: str) -> str:
    if material in ["kůže", "umělá kůže", "veganská eko kůže", "štípenka"]:
        return "leather"
    elif material in ["buklé", "len", "manšestr", "nepravý semiš", "polyester", "umělý len", "umělý samet", "žinylka"]:
        return "fabric"
    else:
        return "UNDEFINED"


def map_additional_material(material: str) -> dict:
    materials = {"contains_metal": 0, "contains_hardwood": 0}
    if material in ["kov", "kovová", "kovové"]:
        materials["contains_metal"] = 1
    elif material in ["dřevo", "masiv", "dřevo masiv"]:
        materials["contains_hardwood"] = 1

    return materials


def parse_beliani_price(price_text: str) -> float:
    return float(price_text.replace(" ", ""))


def process_key_value(key: str, value: str, data_dict: dict):
    if key == "materiál":
        data_dict["cover_material"] = map_material(value)

    elif key == "další materiál":
        additional_material = map_additional_material(value)
        data_dict.update(additional_material)

    elif key in ["šířka", "výška", "hloubka"]:
        data_dict[key] = int(value.replace("cm", "").strip())

    elif key == "výška sedáku":
        data_dict["sit_height"] = int(value.replace("cm", "").strip())


def parse_all_other_beliani_parameters(soup: BeautifulSoup, data_dict: dict):
    description_block = soup.find('div', class_='offerDescriptionBlock')
    if not description_block:
        return

    all_elements = description_block.find_all('div', class_='list_elem')
    for element in all_elements:
        key = element.find('b').text.replace(":", "").strip()
        value = element.find('span').text.lower().strip()

        if not key or not value:
            continue

        if key not in BELIANI_DESCRIPTION_KEYS:
            continue

        process_key_value(key, value, data_dict)


def parse_beliani_link(page_link: str) -> dict:
    try:
        soup = get_soup_parser(page_link)

        main_price = soup.find('span', class_='price_text')
        price_text = main_price.text if main_price else None

        if price_text is None:
            raise Exception("Price not found")

        data_dict = init_data_map()
        data_dict["price"] = parse_beliani_price(price_text)

        parse_all_other_beliani_parameters(soup, data_dict)

        return data_dict

    except requests.RequestException as e:
        print(f"Failed to fetch {page_link}: {e}")
        return {}


def  parse_beliani_links() -> int:
    total_parsed_links = 0
    all_sofas_parsed_links = []
    with open("links-gathered-beliani.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

        for link in links:
            print(f"Parsing link: {link}")
            parsed_data = parse_beliani_link(link.strip())

            if not finalize_parsed_dict(all_sofas_parsed_links, parsed_data):
                print(f"Failed to parse link: {link}")
            else:
                total_parsed_links += 1

    append_parsed_data(all_sofas_parsed_links)
    return total_parsed_links
