# Web Scraping Script

This repository contains a Python script for web scraping data from the Prime Minister's Office of India website.

## Features

- Navigates to the PM India website and waits for a specific link to appear.
- Scrolls the page to load dynamic content.
- Collects news titles, dates, and content from specific div elements.
- Stores the data in a pandas DataFrame and saves it as a CSV file.
- Limits the scraping to 500 titles to avoid overloading.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4
- pandas

## Setup

Install the required packages:

```sh
pip install selenium beautifulsoup4 pandas
