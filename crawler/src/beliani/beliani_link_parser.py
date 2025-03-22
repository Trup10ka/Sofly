import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.util import init_data_map, finalize_parsed_dict, append_parsed_data, get_soup_parser, BELIANI_DESCRIPTION_KEYS, \
    get_selenium_parser, map_key


def map_material(material: str) -> str:
    if material in ["kůže", "umělá kůže", "veganská eko kůže", "štípenka"]:
        return "leather"
    elif material in ["buklé", "len", "manšestr", "nepravý semiš", "polyester", "umělý len", "umělý samet", "žinylka"]:
        return "fabric"
    else:
        return "UNDEFINED"


def map_additional_material(material: str) -> dict:
    materials = {"contains_metal": 0, "contains_hardwood": 0}
    if any(substring in material for substring in ["kov", "kovová", "kovové", "železo", "ocel", "titan", "hliník", "nerez"]):
        materials["contains_metal"] = 1
    elif any(substring in material for substring in ["dřevo", "masiv", "dřevo masiv"]):
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
        mapped_key = map_key(key)
        data_dict[mapped_key] = int(value.replace("cm", "").strip())

    elif key == "výška sedáku":
        data_dict["sit_height"] = int(value.replace("cm", "").strip())


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
    with open("links-gathered-beliani.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

        for link in links:
            print(f"Parsing link: {link}")
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
