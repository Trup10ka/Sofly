from datetime import datetime

from crawler.src.asko.asko_link_gatherer import asko_gather_links
from crawler.src.beliani.beliani_link_gatherer import beliani_gather_links
from crawler.src.veneti.veneti_link_gatherer import veneti_gather_links
from crawler.src.asko.asko_link_parser import parse_asko_links
from loguru import logger
from crawler.src.beliani.beliani_link_parser import parse_beliani_links
from crawler.src.veneti.veneti_link_parser import parse_veneti_links


def gather_all_links() -> int:
    return asko_gather_links() + veneti_gather_links() + beliani_gather_links()

def parse_all_links() -> int:
    return parse_asko_links() + parse_beliani_links() + parse_veneti_links()

if __name__ == '__main__':
    logger.info(f"Starting crawler at {datetime.now()}")
    total_links = gather_all_links()
    logger.info(f"Total links: {total_links}")
    total_parsed_links = parse_all_links()
    logger.info(f"Total parsed links: {total_parsed_links}")
    logger.info(f"Finished crawler at {datetime.now()}")