import requests
import csv
from bs4 import BeautifulSoup

from src.util import init_data_map, ASKO_DESCRIPTION_KEYS


def asko_check_whether_contains_metal(li_value: str) -> bool:
    return any(substring in li_value for substring in ["kov", "kovové", "kovy"])


def asko_check_whether_contains_hardwood(li_value: str) -> bool:
    return any(substring in li_value for substring in ["dřevo", "masiv", "dřevo masiv"])


def parse_asko_price(price_text: str) -> float:
    return float(' '.join(price_text.replace('\xa0', ' ').strip().split(' ')[:-1]).strip().replace(' ', ''))


def get_material(li_value: str) -> str:
    first_element = li_value.split('-', 1)[0].strip()
    if "látka" in first_element:
        return "fabric"
    elif "kůže" in first_element:
        return "leather"
    elif "ekokůže" in first_element or "eko kůže" in first_element:
        return "eco-leather"
    else:
        return "UNDEFINED"


def check_all_th_elements_in_parameters(th_elements, data_dict):
    for th in th_elements:
        if th.text.lower().strip() not in ASKO_DESCRIPTION_KEYS:
            continue

        td_pair_element = th.find_next('td')
        td_value = td_pair_element.text.strip()

        if th.text.lower().strip() == "rozměry":
            dimensions = td_value.split('x')
            data_dict["length"] = int(dimensions[0].split('-')[0])
            data_dict["width"] = int(dimensions[1].split('-')[0])
            data_dict["depth"] = int(dimensions[2].split('-')[0])

        elif th.text.lower().strip() == "výška sedáku":
            data_dict["sit_height"] = int(td_value.strip().split("\n")[0].split('-')[0].strip())


def check_all_li_elements_in_description(li_elements, data_dict):
    for li in li_elements:
        if ":" not in li.text.lower().strip():
            continue
        li_key, li_value = li.text.split(':', maxsplit=1)
        if li_key.lower().strip() not in ASKO_DESCRIPTION_KEYS:
            continue

        if li_key == "konstrukce":
            data_dict["contains_metal"] = 1 if asko_check_whether_contains_metal(li_value) else 0
            data_dict["contains_hardwood"] = 1 if asko_check_whether_contains_hardwood(li_value) else 0

        elif li_key == "potah":
            data_dict["cover_material"] = get_material(li_value)


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
        import time

        response = requests.get(page_link)
        time.sleep(7)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        main_price = soup.find('strong', class_='main-price')
        price_text = main_price.text if main_price else None

        if price_text is None:
            raise Exception("Price not found")

        data_dict = init_data_map()
        data_dict["price"] = parse_asko_price(price_text)
        if not parse_description_div(soup, data_dict):
            raise Exception("Parsing description failed")

        if not parse_product_parameters(soup, data_dict):
            raise Exception("Parsing product parameters failed")

        return data_dict

    except requests.RequestException as e:
        print(f"Failed to fetch {page_link}: {e}")
        return {}


def parse_asko_links() -> int:
    total_parsed_links = 0
    all_sofas_parsed_links = []
    with open("links-gathered-asko.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

        for link in links:
            print(f"Parsing link: {link}")
            parsed_data = parse_link(link.strip())
            if len(parsed_data) == 0:
                continue

            default_data = init_data_map()
            if any(parsed_data[key] == default_data[key] for key in parsed_data):
                raise Exception("Parsing data failed - default value was in the result dict, which means error during parsing")
            all_sofas_parsed_links.append(parsed_data)

    with open("sofa-set.csv", "a", newline='', encoding="utf-8") as csvfile:
        fieldnames = all_sofas_parsed_links[0].keys() if all_sofas_parsed_links else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in all_sofas_parsed_links:
            writer.writerow(data)

    return total_parsed_links
