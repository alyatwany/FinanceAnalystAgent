import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import List, Dict
import re
from urllib.parse import quote
from langchain.tools import tool
from DataExtraction.DataExtractor import EXTRACT
from Schemas.extraction_schemas import get_news_sentiment

def get_google_finance_news(symbol: str) -> List[Dict]:
    """Scrape news from Google Finance"""
    articles = []
    try:
        url = f"https://www.google.com/finance/quote/{symbol}:NASDAQ"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find news articles
        news_items = soup.find_all('div', class_='yY3Lee')
        for item in news_items[:10]:
            try:
                headline_elem = item.find('div', class_='Yfwt5')
                source_elem = item.find('div', class_='sfyJob')
                time_elem = item.find('div', class_='Adak')
                link_elem = item.find('a', class_='z4rs2b')
                
                if headline_elem:
                    articles.append({
                        'headline': headline_elem.get_text(strip=True),
                        'text': '',
                        'date': time_elem.get_text(strip=True) if time_elem else '',
                        'source': source_elem.get_text(strip=True) if source_elem else 'Google Finance',
                        'url': f"https://www.google.com{link_elem['href']}" if link_elem and link_elem.get('href') else ''
                    })
            except Exception as e:
                continue
    except Exception as e:
        print(f"Error fetching from Google Finance: {e}")
    
    return articles

def get_yahoo_finance_news(symbol: str) -> List[Dict]:
    """Scrape news from Yahoo Finance"""
    articles = []
    try:
        url = f"https://finance.yahoo.com/quote/{symbol}/news"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find news articles
        news_items = soup.find_all('li', class_='stream-item')
        for item in news_items[:10]:
            try:
                headline_elem = item.find('h3')
                summary_elem = item.find('p')
                link_elem = item.find('a')
                time_elem = item.find('time')
                
                if headline_elem:
                    articles.append({
                        'headline': headline_elem.get_text(strip=True),
                        'text': summary_elem.get_text(strip=True) if summary_elem else '',
                        'date': time_elem.get('datetime', '') if time_elem else '',
                        'source': 'Yahoo Finance',
                        'url': f"https://finance.yahoo.com{link_elem['href']}" if link_elem and link_elem.get('href') else ''
                    })
            except Exception as e:
                continue
    except Exception as e:
        print(f"Error fetching from Yahoo Finance: {e}")
    
    return articles

def get_seeking_alpha_news(symbol: str) -> List[Dict]:
    """Scrape news from Seeking Alpha"""
    articles = []
    try:
        url = f"https://seekingalpha.com/symbol/{symbol}/news"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find news articles
        news_items = soup.find_all('article')
        for item in news_items[:10]:
            try:
                headline_elem = item.find(['h3', 'h4'])
                summary_elem = item.find('p')
                link_elem = item.find('a')
                time_elem = item.find('time')
                
                if headline_elem:
                    href = link_elem.get('href', '') if link_elem else ''
                    full_url = f"https://seekingalpha.com{href}" if href.startswith('/') else href
                    
                    articles.append({
                        'headline': headline_elem.get_text(strip=True),
                        'text': summary_elem.get_text(strip=True) if summary_elem else '',
                        'date': time_elem.get('datetime', '') if time_elem else '',
                        'source': 'Seeking Alpha',
                        'url': full_url
                    })
            except Exception as e:
                continue
    except Exception as e:
        print(f"Error fetching from Seeking Alpha: {e}")
    
    return articles

def get_marketwatch_news(symbol: str) -> List[Dict]:
    """Scrape news from MarketWatch"""
    articles = []
    try:
        url = f"https://www.marketwatch.com/investing/stock/{symbol.lower()}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find news articles
        news_items = soup.find_all('div', class_='article__content')
        for item in news_items[:10]:
            try:
                headline_elem = item.find(['h3', 'h5'])
                summary_elem = item.find('p')
                link_elem = item.find('a')
                time_elem = item.find('span', class_='article__timestamp')
                
                if headline_elem:
                    href = link_elem.get('href', '') if link_elem else ''
                    full_url = f"https://www.marketwatch.com{href}" if href.startswith('/') else href
                    
                    articles.append({
                        'headline': headline_elem.get_text(strip=True),
                        'text': summary_elem.get_text(strip=True) if summary_elem else '',
                        'date': time_elem.get_text(strip=True) if time_elem else '',
                        'source': 'MarketWatch',
                        'url': full_url
                    })
            except Exception as e:
                continue
    except Exception as e:
        print(f"Error fetching from MarketWatch: {e}")
    
    return articles

@tool
def get_all_news(symbol: str) -> List[Dict]:
    """Fetch news from multiple sources"""
    print(f"Fetching news for {symbol} from multiple sources...\n")
    
    all_articles = []
    
    print(" Fetching from Google Finance...")
    google_articles = get_google_finance_news(symbol)
    all_articles.extend(google_articles)
    print(f"   Found {len(google_articles)} articles")
    
    print(" Fetching from Yahoo Finance...")
    yahoo_articles = get_yahoo_finance_news(symbol)
    all_articles.extend(yahoo_articles)
    print(f"   Found {len(yahoo_articles)} articles")
    
    print(" Fetching from Seeking Alpha...")
    seeking_articles = get_seeking_alpha_news(symbol)
    all_articles.extend(seeking_articles)
    print(f"   Found {len(seeking_articles)} articles")
    
    print("Fetching from MarketWatch...")
    market_articles = get_marketwatch_news(symbol)
    all_articles.extend(market_articles)
    print(f"   Found {len(market_articles)} articles")
    seen = set()
    unique_articles = []
    for article in all_articles:
        if article['headline'] and article['headline'] not in seen:
            seen.add(article['headline'])
            unique_articles.append(article)

    return EXTRACT("get_news_sentiment",json.dumps(unique_articles))



"""
def save_to_json(articles: List[Dict], filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved {len(articles)} articles to {filename}")

def main():
    symbol = input("Enter stock symbol (e.g., AAPL, TSLA, MSFT): ").strip().upper()
    
    articles = get_all_news(symbol)
    
    if articles:
        print(f"\n{'='*60}")
        print(f"Total unique articles found: {len(articles)}")
        print(f"{'='*60}\n")
        
        # Display first 5 articles
        for i, article in enumerate(articles[:5], 1):
            print(f"{i}. {article['headline']}")
            print(f"   Source: {article['source']}")
            print(f"   Date: {article['date']}")
            if article['text']:
                print(f"   Summary: {article['text'][:100]}...")
            print()
        
        # Save to JSON
        filename = f"{symbol}_news.json"
        save_to_json(articles, filename)
        
        # Print full JSON
        print(f"\n{'='*60}")
        print("JSON Output:")
        print(f"{'='*60}\n")
        print(json.dumps(articles, indent=2))
    else:
        print(f"\n❌ No articles found for {symbol}")

if __name__ == "__main__":
    main()""
    """