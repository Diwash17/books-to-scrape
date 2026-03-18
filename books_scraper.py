"""
Web Scraper for Books to Scrape
Extracts book information from https://books.toscrape.com/
"""

import requests
from bs4 import BeautifulSoup
from datetime import date
import json
import csv
import time
from urllib.parse import urljoin


class BooksScraper:
    def __init__(self, base_url="https://books.toscrape.com/"):
        self.base_url = base_url
        self.books_data = []
        self.scrape_date = date.today().isoformat()
    
    def get_page(self, url):
        """Fetch a page with error handling"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_rating(self, soup):
        """Extract rating from star class"""
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        star_element = soup.find('p', class_='star-rating')
        if star_element:
            rating_class = star_element.get('class', [])
            for rating_text in rating_map.keys():
                if rating_text in rating_class:
                    return rating_map[rating_text]
        return None
    
    def scrape_book_details(self, book_url):
        """Scrape details from a book's detail page"""
        soup = self.get_page(book_url)
        if not soup:
            return None
        
        # Extract book title
        title_element = soup.find('h1')
        name = title_element.text.strip() if title_element else "N/A"
        
        # Extract description
        description_element = soup.find('div', id='product_description')
        if description_element:
            description_p = description_element.find_next_sibling('p')
            description = description_p.text.strip() if description_p else "N/A"
        else:
            description = "N/A"
        
        # Extract price (excluding tax)
        price_element = soup.find('p', class_='price_color')
        price = price_element.text.strip() if price_element else "N/A"
        
        # Extract information from the table
        table = soup.find('table', class_='table table-striped')
        upc = "N/A"
        tax = "N/A"
        availability = "N/A"
        
        if table:
            rows = table.find_all('tr')
            for row in rows:
                header = row.find('th')
                value = row.find('td')
                if header and value:
                    header_text = header.text.strip()
                    if header_text == "UPC":
                        upc = value.text.strip()
                    elif header_text == "Tax":
                        tax = value.text.strip()
                    elif header_text == "Availability":
                        availability = value.text.strip()
        
        # Extract rating
        rating = self.extract_rating(soup)
        
        book_data = {
            "name": name,
            "url": book_url,
            "scrape_date": self.scrape_date,
            "description": description,
            "price": price,
            "tax": tax,
            "availability": availability,
            "upc": upc,
            "rating": rating
        }
        
        return book_data
    
    def scrape_all_books(self):
        """Scrape all books across all pages"""
        current_url = self.base_url
        page_num = 1
        
        while current_url:
            print(f"Scraping page {page_num}...")
            soup = self.get_page(current_url)
            
            if not soup:
                break
            
            # Find all book containers
            books = soup.find_all('article', class_='product_pod')
            
            for book in books:
                # Get the book detail page URL
                h3 = book.find('h3')
                if h3:
                    link = h3.find('a')
                    if link and link.get('href'):
                        relative_url = link['href']
                        # Convert relative URL to absolute
                        book_url = urljoin(current_url, relative_url)
                        
                        # Scrape book details
                        book_data = self.scrape_book_details(book_url)
                        if book_data:
                            self.books_data.append(book_data)
                            print(f"  ✓ Scraped: {book_data['name']}")
                        
                        # Be polite - add a small delay
                        time.sleep(0.5)
            
            # Find next page link
            next_button = soup.find('li', class_='next')
            if next_button:
                next_link = next_button.find('a')
                if next_link and next_link.get('href'):
                    next_relative_url = next_link['href']
                    current_url = urljoin(current_url, next_relative_url)
                    page_num += 1
                else:
                    current_url = None
            else:
                current_url = None
        
        print(f"\nScraping complete! Total books scraped: {len(self.books_data)}")
    
    def save_to_json(self, filename="books_data.json"):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.books_data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    
    def save_to_csv(self, filename="books_data.csv"):
        """Save scraped data to CSV file"""
        if not self.books_data:
            print("No data to save!")
            return
        
        fieldnames = ["name", "url", "scrape_date", "description", "price", 
                     "tax", "availability", "upc", "rating"]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.books_data)
        print(f"Data saved to {filename}")


def main():
    print("=" * 60)
    print("Books to Scrape - Web Scraper")
    print("=" * 60)
    print()
    
    # Initialize scraper
    scraper = BooksScraper()
    
    # Scrape all books
    scraper.scrape_all_books()
    
    # Save to both formats
    scraper.save_to_json()
    scraper.save_to_csv()
    
    print("\n✓ Scraping completed successfully!")


if __name__ == "__main__":
    main()
