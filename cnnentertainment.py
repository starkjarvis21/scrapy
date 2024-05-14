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
        all_news = soup.select("div.container_lead-plus-headlines-with-images__item.container_lead-plus-headlines-with-images__item--type-section a")
        for news in all_news:
            # Try to find the title within the link element
            title_span = news.find('span')
            title = title_span.get_text(strip=True) if title_span else "No title found"
            relative_link = news.get('href')
            if relative_link:
                full_link = requests.compat.urljoin(url, relative_link)
                yield {'title': title, 'link': full_link}

def parse_article(article_url):
    html_content = fetch_page(article_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        content = ' '.join([p.get_text(strip=True) for p in soup.select('div.article__content p.paragraph.inline-placeholder.vossi-paragraph-primary-core-light')])
        return content

def main():
    url = 'https://edition.cnn.com/entertainment'
    category = url.split('/')[-1]

    with open('cnn_entertainment.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Content', 'Link', 'Source', 'Title'])  # Writing the headers of CSV

        for news_item in parse_homepage(url):
            article_content = parse_article(news_item['link'])
            # Write the data in the specified order
            writer.writerow([category, article_content, news_item['link'], 'CNN', news_item['title']])

if __name__ == "__main__":
    main()
