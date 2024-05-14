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
        all_news_divs = soup.select("div.wide-tease-item__info-wrapper")
        for div in all_news_divs:
            links = div.find_all('a')
            if len(links) > 1:  # Check if there are at least two links
                news = links[1]  # Select the second link
                title_tag = news.find('h2')
                title = title_tag.get_text(strip=True) if title_tag else "No title found"
                relative_link = news.get('href')
                if relative_link:
                    full_link = requests.compat.urljoin(url, relative_link)
                    yield {'title': title, 'link': full_link}

def parse_article(article_url):
    html_content = fetch_page(article_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        content = ' '.join([p.get_text(strip=True) for p in soup.select('div.article-body__content p')])
        return content

def main():
    url = 'https://www.nbcnews.com/business'
    category = url.split('/')[-1] if 'culture-matters' not in url else 'entertainment'

    with open('nbcnews_business_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Content', 'Link', 'Source', 'Title'])  # Writing the headers of CSV

        for news_item in parse_homepage(url):
            article_content = parse_article(news_item['link'])
            # Write the data in the specified order
            writer.writerow([category, article_content, news_item['link'], 'NBC', news_item['title']])

if __name__ == "__main__":
    main()
