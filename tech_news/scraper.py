import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    time.sleep(1)

    headers_trybe = {"user-agent": "Fake user-agent"}

    try:
        response = requests.get(url, headers=headers_trybe, timeout=3)
    except requests.Timeout:
        return None

    if response.status_code != 200:
        return None

    return response.text


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)

    updates_list = selector.css(".entry-thumbnail a::attr(href)").getall()

    return updates_list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)

    next_page_url = selector.css(".next::attr(href)").get()

    return next_page_url


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
