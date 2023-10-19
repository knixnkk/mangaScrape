# Web Scraping and Image Conversion Scripts

This repository contains two Python scripts designed for web scraping, image downloading, conversion to PDF, and file organization. Each script serves a unique purpose and utilizes different libraries and methods.

## Script 1: BeautifulSoup-Based Web Scraping and Asynchronous Image Conversion

- **Libraries Used**: `requests`, `BeautifulSoup`, `aiohttp`, `PIL`, and more.

- **Functionality**: Script 1 leverages BeautifulSoup for web scraping and asynchronous image conversion. It extracts JSON data from web pages, processes it to collect image URLs, and organizes generated PDF files into folders based on chapter titles.

## Script 2: Selenium-Based Web Scraping and Image Handling

- **Libraries Used**: `Selenium`, `requests`, `PIL`, `img2pdf`, and more.

- **Functionality**: Script 2 utilizes Selenium for web scraping and page interaction. It scrolls down web pages, selects chapters, collects image URLs, and handles page navigation. The script is capable of retries and checks for the presence of the Microsoft Edge browser process.

These scripts are tailored for specific use cases and may require customization to work with different websites or scenarios. They offer insights into various techniques for web scraping, image handling, and file organization in a scripted environment.

Please refer to each script's documentation and requirements for detailed usage instructions and any necessary installations.

Feel free to explore and adapt these scripts to meet your specific needs.

**Note**: Ensure you have the required Python libraries and web drivers set up as specified in the respective script's documentation.
