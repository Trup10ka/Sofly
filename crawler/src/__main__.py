from src.asko.asko_link_gatherer import asko_gather_links
from src.beliani.beliani_link_gatherer import beliani_gather_links
from src.veneti.veneti_link_gatherer import veneti_gather_links


def gather_all_links() -> int:
    return asko_gather_links() + veneti_gather_links() + beliani_gather_links()

if __name__ == '__main__':
    total_links = gather_all_links()
    print(f"Total links: {total_links}")
    # parse_links()
    pass