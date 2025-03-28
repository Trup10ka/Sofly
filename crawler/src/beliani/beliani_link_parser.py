import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from crawler.src.util import init_data_map, finalize_parsed_dict, append_parsed_data, get_soup_parser, BELIANI_DESCRIPTION_KEYS, \
    get_selenium_parser, map_key


def map_material(data_dict: dict, material: str):
    if material in ["kůže", "umělá kůže", "veganská eko kůže", "štípenka"]:
        data_dict["material_leather"] = 1
    elif material in ["buklé", "len", "manšestr", "nepravý semiš", "polyester", "umělý len", "umělý samet", "žinylka"]:
        data_dict["material_fabric"] = 1
    else:
        data_dict["material_none"] = 1

def define_type_of_furniture(data_dict: dict, furniture_type: str) -> None:
    if any(sofa in furniture_type for sofa in ["pohovka", "gauč", "lenoška"]):
        data_dict["is_sofa"] = 1
    elif any(chair in furniture_type for chair in ["židle", "židlí", "židličky", "židlička"]):
        data_dict["is_chair"] = 1
    elif "stůl" in furniture_type:
        data_dict["is_table"] = 1

def parse_beliani_price(price_text: str) -> float:
    return float(price_text.replace(" ", ""))


def process_key_value(key: str, value: str, data_dict: dict):
    if key == "materiál":
        map_material(data_dict, value)

    elif key in ["šířka", "výška", "hloubka"]:
        data_dict["dimensions"] = data_dict["dimensions"] + int(value.replace("cm", "").strip())

    elif key == "typ":
        define_type_of_furniture(data_dict, value)


def parse_all_other_beliani_parameters(selenium_driver: WebDriver, data_dict: dict):
    try:
        description_block = selenium_driver.find_elements(By.CLASS_NAME, 'offerDescriptionBlock')
        description_block_one = description_block[1].text
        description_block_two = description_block[2].text
        description_block = [line for line in (description_block_one + description_block_two).split("\n") if ":" in line]

        for description in description_block:
            key, value = description.split(":", 1)
            key = key.strip().lower()
            value = value.strip().lower()
            process_key_value(key, value, data_dict)

        if not description_block:
            return


    except Exception as e:
        print(f"Error while parsing parameters: {e}")


def parse_beliani_link(page_link: str, selenium_driver: WebDriver) -> dict:
    try:
        selenium_driver.get(page_link)

        time.sleep(3)

        main_price = selenium_driver.find_element(By.CLASS_NAME, 'price_text')
        price_text = main_price.text if main_price else None

        data_dict = init_data_map()

        if price_text is None:
            data_dict["ERROR"] = "Price not found"
            return data_dict

        data_dict["price"] = parse_beliani_price(price_text)

        parse_all_other_beliani_parameters(selenium_driver, data_dict)

        return data_dict

    except Exception as e:
        print(f"Failed to parse {page_link}: {e}")
        return {}


def parse_beliani_links() -> int:
    total_parsed_links = 0
    all_sofas_parsed_links = []
    selenium_driver = get_selenium_parser("https://www.beliani.cz")
    with open("crawler/links-gathered-beliani.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

        for link in links:
            print(f"Parsing link: {link.strip()}")
            parsed_data = parse_beliani_link(link.strip(), selenium_driver)

            if parsed_data.get("ERROR"):
                all_sofas_parsed_links.append(parsed_data)
                continue

            if not finalize_parsed_dict(all_sofas_parsed_links, parsed_data):
                print(f"Failed to parse link: {link}")
            else:
                total_parsed_links += 1

    append_parsed_data(all_sofas_parsed_links)
    return total_parsed_links
