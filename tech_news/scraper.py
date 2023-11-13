import requests
import time
from parsel import Selector
from tech_news.database import create_news


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

    updates_list = selector.css("a.entry-thumbnail::attr(href)").getall()

    return updates_list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)

    next_page_url = selector.css("a.next::attr(href)").get()

    return next_page_url


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)

    url = selector.css("div.pk-share-buttons-wrap::attr(data-share-url)").get()
    title = selector.css("h1.entry-title::text").get().strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.fn a::text").get().strip()

    reading_time = int(
        selector.css("li.meta-reading-time::text").re_first(r"\d+")
    )

    summary = "".join(
        selector.css("div.entry-content > p:first-of-type *::text").getall()
    ).strip()

    category = selector.css("span.label::text").get()

    news_data = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }

    return news_data


# Requisito 5
def get_tech_news(amount):
    URL_BLOG_TRYBE = "https://blog.betrybe.com/"

    conteudo_url_atual = fetch(URL_BLOG_TRYBE)

    lista_urls_noticias = scrape_updates(conteudo_url_atual)

    while len(lista_urls_noticias) < amount:
        url_proxima_pagina = scrape_next_page_link(conteudo_url_atual)
        conteudo_url_atual = fetch(url_proxima_pagina)
        lista_urls_noticias.extend(scrape_updates(conteudo_url_atual))

    lista_urls_noticias_selecionadas = []
    index = 0

    while len(lista_urls_noticias_selecionadas) < amount:
        lista_urls_noticias_selecionadas.append(lista_urls_noticias[index])
        index += 1

    lista_dicionarios_noticias = []

    for url_noticia_selecionada in lista_urls_noticias_selecionadas:
        dict_noticia = scrape_news(url_noticia_selecionada)
        lista_dicionarios_noticias.append(dict_noticia)

    create_news(lista_dicionarios_noticias)

    return lista_dicionarios_noticias
