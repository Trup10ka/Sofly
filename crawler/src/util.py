import csv
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ASKO_DESCRIPTION_KEYS = ("konstrukce", "potah", "rozměry (š x v x h)", "výška sedáku")
VENETI_DESCRIPTION_KEYS = ("rám", "materiál potahu", "výška", "šířka", "hloubka", "výška sedu")
BELIANI_DESCRIPTION_KEYS = ("další materiál", "materiál", "výška", "šířka", "hloubka", "výška sedáku")

BELIANI_COOKIE = {
        "name": "cookie_warning_done",
        "value": "1",
        "domain": "www.beliani.cz",
        "path": "/",
        "secure": False,
        "httpOnly": False,
        "sameSite": "None",
        "expiry": 1778169315  # Convert "Tue, 10 Mar 2026 13:15:15 GMT" to UNIX timestamp
}

def get_selenium_parser(link: str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    driver = webdriver.Chrome(options=options)

    driver.get("https://www.beliani.cz")

    driver.add_cookie(BELIANI_COOKIE)

    driver.get(link)

    time.sleep(3)

    return driver

def get_soup_parser(link: str) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(link, headers=headers)
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
    else:
        data_dict["ERROR"] = 0
    all_sofas_parsed_links.append(data_dict)
    print("Parsed data: ", data_dict)
    return True

def map_key(key: str) -> str:
    match key:
        case "šířka":
            return "length"
        case "výška":
            return "width"
        case "hloubka":
            return "depth"
        case "výška sedu":
            return "sit_height"
        case "materiál" | "materiál potahu":
            return "cover_material"
        case _:
            return key

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
