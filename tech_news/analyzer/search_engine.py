from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}

    noticias = []

    for noticia in search_news(query):
        noticias.append((noticia["title"], noticia["url"]))

    return noticias


# Requisito 8
def search_by_date(date):
    try:
        date_iso = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")

    date_db = date_iso.strftime("%d/%m/%Y")

    query = {"timestamp": date_db}

    noticias = []

    for noticia in search_news(query):
        noticias.append((noticia["title"], noticia["url"]))

    return noticias


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
