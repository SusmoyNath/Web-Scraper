# 🌐 Web Scraper

A flexible, Python-based web scraping utility to extract data from a curated list of URLs. This project logs the success and failure of requests, handles exceptions gracefully, and outputs results to a JSON file. Designed for beginners and experienced developers alike.

---

## 🚀 Features

- Scrapes a list of URLs from a file (`urls.txt`)
- Automatically logs:
  - ✅ Successful scrapes
  - ❌ Failed requests (with error reasons)
- Saves the successfully scraped data into `scraped_data.json`
- Provides a cleaned list of valid URLs via `urls_clean.txt`
- Modular and easily extendable

---

## 📂 Project Structure


Web-Scraper/
├── web-scraper.py          # Main scraping logic
├── urls.txt                # Input URLs to scrape
├── urls_clean.txt          # Output of working URLs (auto-generated)
├── scraped_data.json       # Final scraped content (auto-generated)
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation


---

## 🛠️ Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`
- `urllib3`
- `logging`

Install dependencies:


pip install -r requirements.txt


---

## 🧠 Usage

1. Add the URLs you want to scrape into `urls.txt`, one per line.
2. Run the scraper:

```bash
python web-scraper.py
```

3. Check your results:
   - `scraped_data.json`: Scraped HTML or textual content
   - `urls_clean.txt`: Filtered URLs that worked
   - Logs in the console will tell you which URLs failed

---

## 📓 Example Output

**Console Log**
```
2025-04-22 23:35:10,039 - INFO - Scraped https://example.com/
2025-04-22 23:35:21,373 - ERROR - Failed to fetch https://www.amazon.com/s?k=laptops: 503 Server Error
```

**scraped_data.json**
```json
[
  {
    "url": "https://example.com",
    "content": "<!doctype html>..."
  },
  ...
]
```

---

## ⚙️ Customization

Want to scrape specific elements or parse structured data like tables or product listings? Just extend the logic in `web-scraper.py` using BeautifulSoup!

```python
soup = BeautifulSoup(response.text, 'html.parser')
title = soup.title.string
```

---

## ❗ Known Issues

- Some pages (like Amazon) actively block bots and may require headers, user-agent spoofing, or Selenium.
- API URLs that need authentication (e.g. NYT, Coindesk) may return `401 Unauthorized` or `403 Forbidden`.

---


> Built with curiosity, Python, and lots of trial & error 🚀
