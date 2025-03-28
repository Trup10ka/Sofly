import requests
from bs4 import BeautifulSoup
from loguru import logger

from crawler.src.util import init_data_map, ASKO_DESCRIPTION_KEYS, finalize_parsed_dict, append_parsed_data, \
    get_soup_parser, has_type_been_assigned


def asko_check_whether_contains_metal(li_value: str) -> bool:
    return any(substring in li_value for substring in ["kov", "kovové", "kovy"])


def asko_check_whether_contains_hardwood(li_value: str) -> bool:
    return any(substring in li_value for substring in ["dřevo", "masiv", "dřevo masiv"])

def get_asko_price(data_dict, soup: BeautifulSoup) -> str | None:
    try:
        main_price = soup.find('strong', class_='main-price')
        main_price_with_discount = soup.find('span', class_='price-value__action-text')
        main_price_with_discount = main_price_with_discount.find('strong') if main_price_with_discount else None

        if main_price_with_discount is None and main_price is None:
            raise AttributeError("Price not found")
        else:
             return main_price_with_discount.text if main_price_with_discount else main_price.text
    except AttributeError:
        price_text = "-1"
        data_dict["ERROR"] = 1
        data_dict["price"] = price_text
        return None

def parse_asko_price(price_text: str) -> float:
    return float(' '.join(price_text.replace('\xa0', ' ').strip().split(' ')[:-1]).strip().replace(' ', ''))


def set_material(data_dict: dict, li_value: str) -> None:
    first_element = li_value.split('-', 1)[0].strip()
    if "látka" in first_element:
        data_dict["material_fabric"] = 1
    elif "kůže" in first_element:
        data_dict["material_leather"] = 1
    elif "ekokůže" in first_element or "eko kůže" in first_element:
        data_dict["material_leather"] = 1
    else:
        data_dict["material_none"] = 1


def check_all_th_elements_in_parameters(th_elements, data_dict):
    for th in th_elements:
        if th.text.lower().strip() not in ASKO_DESCRIPTION_KEYS:
            continue

        td_pair_element = th.find_next('td')
        td_value = td_pair_element.text.strip()

        if th.text.lower().strip().split(' ')[0] == "rozměry":
            td_value_parsed = td_value.replace('cm', '').strip()
            dimensions = td_value_parsed.split(',')[0].split('x')
            data_dict["dimensions"] = int(dimensions[0].split('-')[0]) + int(dimensions[1].split('-')[0]) + int(dimensions[2].split('-')[0])

def determine_type_of_furniture(data_dict, value: str) -> None:
    if any(substring.lower().strip() in value.lower().strip() for substring in ["židle", "stolička", "židlí", "stoličky"]):
        data_dict["is_chair"] = 1
    elif any(substring.lower().strip() in value.lower().strip() for substring in ["stůl", "konferenční", "jídelní", "kancelářský"]):
        data_dict["is_table"] = 1
    elif any(substring.lower().strip() in value.lower().strip() for substring in ["pohovka", "gauč", "křeslo", "křesla", "dvojsedák", "trojsedák"]):
        data_dict["is_sofa"] = 1

def check_all_li_elements_in_description(li_elements, data_dict):
    for index, li in enumerate(li_elements):

        if index == 0 and not has_type_been_assigned(data_dict):
            determine_type_of_furniture(data_dict, li)
            continue

        if ":" not in li.text.lower().strip():
            continue

        li_key, li_value = li.text.split(':', maxsplit=1)
        li_key = li_key.split(' ', 1)[0].lower().strip()
        if li_key.split(' ', 1)[0].lower().strip() not in ASKO_DESCRIPTION_KEYS:
            continue

        # TODO: implement detecting what type of furniture it is

        elif li_key == "potah":
            set_material(data_dict, li_value)


def parse_description_div(soup: BeautifulSoup, data_dict) -> bool:
    description_div = soup.find('div', itemprop='description')
    if description_div:
        li_elements = description_div.find_all('li')
        check_all_li_elements_in_description(li_elements, data_dict)
        return True
    else:
        return False


def parse_product_parameters(soup: BeautifulSoup, data_dict) -> bool:
    parameters_div = soup.find('div', id='js-product-parameters')
    if parameters_div:
        th_elements = parameters_div.find_all('th')
        check_all_th_elements_in_parameters(th_elements, data_dict)
        return True
    else:
        return False


def parse_link(page_link: str) -> dict:
    try:
        soup = get_soup_parser(page_link)

        data_dict = init_data_map()
        price_text = get_asko_price(data_dict, soup)
        type_of_furniture_header = soup.find('h1', class_='product-title-desktop').text.strip()

        determine_type_of_furniture(data_dict, type_of_furniture_header)

        if price_text is None:
            raise Exception("Price not found")

        data_dict["price"] = parse_asko_price(price_text)
        if not parse_description_div(soup, data_dict):
            raise Exception("Parsing description failed")

        if not parse_product_parameters(soup, data_dict):
            raise Exception("Parsing product parameters failed")

        return data_dict

    except requests.RequestException as e:
        logger.error(f"Failed to fetch {page_link}: {e}")
        return {}


def parse_asko_links() -> int:
    total_parsed_links = 0
    all_sofas_parsed_links = []
    with open("crawler/links-gathered-asko.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

        for link in links:
            logger.info(f"Parsing link: {link.strip()}")
            parsed_data = parse_link(link.strip())
            if len(parsed_data) == 0:
                continue

            if not finalize_parsed_dict(all_sofas_parsed_links, parsed_data):
                logger.error(f"Failed to parse link: {link}")
            else:
                total_parsed_links += 1

        append_parsed_data(all_sofas_parsed_links)
        return total_parsed_links
