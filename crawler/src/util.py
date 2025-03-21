import csv
import time

import requests
from bs4 import BeautifulSoup

ASKO_DESCRIPTION_KEYS = ("konstrukce", "potah", "rozměry (š x v x h)", "výška sedáku")
VENETI_DESCRIPTION_KEYS = ("konstrukce", "potah", "rozměry", "výška sedáku")
BELIANI_DESCRIPTION_KEYS = ("konstrukce", "potah", "rozměry", "výška sedáku")

def get_soup_parser(link: str) -> BeautifulSoup:
    response = requests.get(link)
    time.sleep(3)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def append_parsed_data(all_sofas_parsed_links: list) -> None:
    with open("sofa-set.csv", "a", newline='', encoding="utf-8") as csvfile:
        fieldnames = all_sofas_parsed_links[0].keys() if all_sofas_parsed_links else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        for data in all_sofas_parsed_links:
            writer.writerow(data)

def finalize_parsed_dict(all_sofas_parsed_links: list, data_dict: dict) -> bool:
    if len(data_dict) == 0:
        return False

    default_data = init_data_map()
    if any(data_dict[key] == default_data[key] for key in data_dict):
        data_dict["ERROR"] = 1
    data_dict["ERROR"] = 0
    all_sofas_parsed_links.append(data_dict)
    return True

def init_data_map() -> dict:
    return {
        "length": 0,
        "width": 0,
        "depth": 0,
        "cover_material": "BLANK",
        "sit_height": 0,
        "contains_metal": -1,
        "contains_hardwood": -1,
        "price": 0
    }
