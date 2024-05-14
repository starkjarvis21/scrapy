import requests
from bs4 import BeautifulSoup
import csv

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_homepage(url):
    html_content = fetch_page(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.select('h3 a')
        return [{'title': article.get_text(strip=True), 'link': article['href']} for article in articles if article['href']]
    else:
        return []

def fetch_article_content(article_url):
    html_content = fetch_page(article_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        content_section = soup.select_one('div.post--content')
        return content_section.get_text(strip=True) if content_section else "No content found"

def main():
    url = 'https://www.herald.co.zw/category/articles/top-stories/'
    articles_info = parse_homepage(url)

    with open('herald_news_articles.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Category','Content','Link','Source','Title'])  # Writing the headers of the CSV file

        for article in articles_info:
            content = fetch_article_content(article['link'])
            # Write the data in the specified order
            writer.writerow([article['title'], article['link'], content])

if __name__ == "__main__":
    main()
