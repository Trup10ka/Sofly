from src.asko.asko_link_gatherer import asko_gather_links
from src.beliani.beliani_link_gatherer import beliani_gather_links
from src.beliani.beliani_link_parser import parse_beliani_links
from src.veneti.veneti_link_gatherer import veneti_gather_links
from src.veneti.veneti_link_parser import parse_veneti_links


def gather_all_links() -> int:
    return asko_gather_links() + veneti_gather_links() + beliani_gather_links()

def parse_all_links() -> int:
    # return parse_asko_links() + parse_beliani_links()
    # return parse_asko_links()
    # return parse_beliani_links()
    return parse_veneti_links()

if __name__ == '__main__':
    # total_links = gather_all_links()
    # print(f"Total links: {total_links}")
    parse_all_links()
    pass