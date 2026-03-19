# Books to Scrape Web Scraper

This is a Python-based web scraper built to extract book information from [Books to Scrape](https://books.toscrape.com/).

## Objective
The scraper fulfills the following requirements:
- Navigates through all 50 pages automatically (pagination).
- Visits each book's individual detail page.
- Extracts specific fields (Title, URL, Date, Description, Price, Tax, Availability, UPC, and Rating).
- Stores the final result in structured formats (`JSON` and `CSV`).

## Code Quality

This project adheres to **PEP 8** standards for Python code style.
- **Pylint Score:** 9.75/10
- Clean import structure and comprehensive docstrings.

## Setup Instructions

1. **Install Python 3** (if you haven't already).
2. **Install Required Libraries**:
   Run the following command in your terminal to install the dependencies (`requests` and `beautifulsoup4`):
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Execute the scraper by running the following command in your terminal:

```bash
python books_scraper.py
```

*Note: The script includes a 0.5-second delay between requests to avoid overloading the website. Since there are 1,000 books, it will take roughly 8-10 minutes to finish.*

## Output Format

Once the script finishes, it will automatically generate two files in the same directory:
- `books_data.json`
- `books_data.csv`

### Extracted Data Fields
| Field | Description |
|-------|-------------|
| `name` | Book title |
| `url` | Absolute URL of the book detail page |
| `scrape_date` | Date when the scraper was run |
| `description` | Product description from the detail page |
| `price` | Book price |
| `tax` | Tax amount |
| `availability` | Availability text (e.g., "In stock (22 available)") |
| `upc` | UPC number |
| `rating` | Book rating (1-5) |

### JSON Output Example
```json
{
  "name": "A Light in the Attic",
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "scrape_date": "2026-03-18",
  "description": "It's hard to imagine a world without A Light in the Attic...",
  "price": "£51.77",
  "tax": "£0.00",
  "availability": "In stock (22 available)",
  "upc": "a897fe39b1053632",
  "rating": 3
}
```



