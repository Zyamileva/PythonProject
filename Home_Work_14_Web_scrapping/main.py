import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

import pandas as pd

import requests
from bs4 import BeautifulSoup
import csv

import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
DAYS_FILTER = 7


def get_page(url: str) -> None | BeautifulSoup:
    """Retrieve and parse a web page.

    Args:
        url: The URL of the web page to retrieve.

    Returns:
        A BeautifulSoup object representing the parsed HTML content, or None if an error occurs.
    """

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logging.exception("Ошибка загрузки сайта: %s", e)
        return None


def parse_news(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Parse news articles from a BeautifulSoup object.

    Args:
        soup: A BeautifulSoup object representing the HTML content to parse.

    Returns:
        A list of dictionaries, where each dictionary contains the title, link, date, and summary of a news article.
    """
    news_list = []
    articles = soup.find_all(
        "div", class_="article__content-col article__content-col--right"
    )

    today = datetime.now()
    date_limit = today - timedelta(days=DAYS_FILTER)
    for article in articles:
        try:
            title = article.find("h3", class_="article__title").text.strip()
            link_tag = article.find("a")
            link = (
                link_tag["href"]
                if link_tag and link_tag.has_attr("href")
                else "Ссылка отсутствует"
            )
            date_str = article.find("div", class_="article__date").text.strip()
            summary = article.find("p").text.strip()

            news_date = datetime.strptime(date_str, "%d.%m.%y")

            if news_date >= date_limit:
                news_list.append(
                    {"title": title, "link": link, "date": date_str, "summary": summary}
                )
        except (AttributeError, ValueError) as e:
            logging.exception("Ошибка парсинга сайта: %s", e)
            continue
    return news_list


def save_to_csv(data: List[Dict[str, Any]], filename="news.csv"):
    """Save data to a CSV file.

    Args:
        data: A list of dictionaries to write to the CSV file.
        filename: The name of the CSV file (default is "news.csv").

    Returns:
        None
    """
    file_exists = os.path.exists(filename)

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "link", "date", "summary"])

        if not file_exists:
            writer.writeheader()

        writer.writerows(data)


def show_statistics(data: List[Dict[str, Any]]):
    """Display publication statistics.

    Args:
        data: A list of dictionaries, where each dictionary contains news data including a "date" field.

    Returns:
        None
    """
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%y")
    stats = df["date"].value_counts().sort_index()
    print("\nСтатистика публикаций за последние 7 дней:")
    print(stats)


def main():
    num = 1
    URL = "https://odessa.online/ru/category/news/"
    news = []
    while True:
        url_page = URL if num == 1 else f"{URL}page/{num}/"
        soup = get_page(url_page)
        if soup is not None:
            if new_news := parse_news(soup):
                news += new_news
            else:
                break
        num += 1

    save_to_csv(news)
    show_statistics(news)


if __name__ == "__main__":
    main()
