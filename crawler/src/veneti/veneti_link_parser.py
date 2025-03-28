import re

from bs4 import BeautifulSoup
from requests import RequestException
from loguru import logger
from crawler.src.util import get_soup_parser, init_data_map, finalize_parsed_dict, map_key, append_parsed_data


def assign_material(data_dict, value):
    if value in ["látka", "textil"]:
        data_dict["material_fabric"] = 1
    elif value in ["kůže", "koženka"]:
        data_dict["material_leather"] = 1
    else:
        data_dict["material_none"] = 1


def assign_type_of_furniture(data_dict, value):
    if any(mapped_key in value.lower() for mapped_key in ["židle", "stolička", "židlí", "stoličky"]):
        data_dict["is_chair"] = 1

    elif any(mapped_key in value.lower() for mapped_key in ["stůl", "konferenční", "jídelní", "kancelářský"]):
        data_dict["is_table"] = 1
    elif any(mapped_key in value.lower() for mapped_key in ["pohovka", "gauč", "křeslo", "křesla"]):
        data_dict["is_sofa"] = 1


def process_value(data_dict, value, key):
    mapped_key = map_key(key.lower().strip())
    value = value.text.strip().lower()

    if mapped_key in ["width", "length", "depth"]:
        assign_material(data_dict, value)
        return
    assign_type_of_furniture(data_dict, value)

    if mapped_key in ["width", "length", "depth"]:
        data_dict["dimensions"] = data_dict["dimensions"] + float(re.search(r'\d+', value).group())


def parse_veneti_price(price_text: str) -> float:
    cleaned_price_text = re.sub(r'[^\d,.-]', '', price_text)
    return float(cleaned_price_text.replace(",", "."))

# TODO: implement first checking what type of furniture it is, then deside the procedure how to parse it
def parse_veneti_link(page_link: str) -> dict:
    try:
        soup = get_soup_parser(page_link)

        main_price = soup.find('span', class_='current-price-value')
        price_text = main_price.text if main_price else None
        if price_text is None:
            error_dict = init_data_map()
            error_dict["ERROR"] = 1
            return error_dict

        data_dict = init_data_map()
        data_dict["price"] = parse_veneti_price(price_text)

        keys = soup.find_all('dt', class_='name')
        values = soup.find_all('dd', class_='value')

        for index, key in enumerate(keys):
            process_value(data_dict, values[index], key.text)

        return data_dict

    except RequestException as e:
        logger.error(f"Failed to fetch {page_link}: {e}")
        return {}


def parse_veneti_links() -> int:
    total_parsed_links = 0
    all_sofas_parsed_links = []
    with open("crawler/links-gathered-veneti.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

        for link in links:
            logger.info(f"Parsing link: {link}")
            parsed_data = parse_veneti_link(link.strip())
            if len(parsed_data) == 0:
                continue

            if not finalize_parsed_dict(all_sofas_parsed_links, parsed_data):
                logger.error(f"Failed to parse link: {link}")
            else:
                total_parsed_links += 1
    append_parsed_data(all_sofas_parsed_links)
    return total_parsed_links
