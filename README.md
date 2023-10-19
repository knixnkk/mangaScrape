# Web Scraping and Image Conversion Scripts

__This repository contains two Python scripts for web scraping, image downloading, conversion to PDF, and file organization. Each script serves a different purpose and utilizes different libraries. Below, you'll find a brief summary of each script's functionality:__

## Script 1: Web Scraping with BeautifulSoup and Asynchronous Image Conversion
__This script uses libraries such as requests, BeautifulSoup, and aiohttp for web scraping.

It extracts JSON data from web pages and processes it to collect image URLs.

The script organizes the generated PDF files into folders based on chapter titles.

Asynchronous image downloading and conversion are handled using aiohttp.
__
## Script 2: Selenium-Based Web Scraping and Image Handling
__
Script 2 uses Selenium for web scraping and interaction with web pages.

It scrolls down web pages, selects chapters, and collects image URLs.

The script handles page navigation, chapter selection, and checks if the Microsoft Edge browser process is running.

Retries are managed in case of errors, and image extensions are checked.

These scripts are designed for specific use cases and may require customization to work with different websites or scenarios. They demonstrate various techniques for web scraping, image handling, and file organization in a scripted environment.

Feel free to explore each script for more details and to adapt them to your specific needs.
__
### Note: Be sure to review the requirements for each script, including necessary Python libraries and web drivers.
