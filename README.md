# Two OpenLibrary Web-Scrapers

Two Python-based web scrapers using BS4 and Selenium respectively.

## Motivation
As an person who has an avid interest in classic novels, I'm always on the hunt for more interesting selections to read. After learning Python and webscraping, I thought I could employ these skills for my own purposes, such as going onto certain online book websites to gather well-rated classic novels to add to my reading list without having to personally click and investigate each book for the relevant information. I've been on the Open Library website every now and then and its classics section had 80 pages that would have taken me far too long to comb through, so I decided to attempt web scraping instead.

## Requirements for Web-Scraper BS4
- Python 3.x
- Beautiful Soup
- Requests
- MySQL
Please note that inserting the scraped data into MySQL uses environment variables that store your MySQL username and password, which would need to be configured on your local device.

## Requirements for Web-Scraper Selenium
- Python 3.x
- Selenium
- ChromeDriver

## Remarks ##
The number of pages to scrape is adjustable for both web-scraping programs. However, since the number of ratings on OpenLibrary drop significantly after page 10, I set a default of 10 pages as scraping beyond that yields very similar results.

