# Cartoon reading Scrape

This repository contains a Python script designed to download, convert, and merge images from a specific website into PDF files. The script utilizes the Selenium library for web automation and some image processing libraries for image-to-PDF conversion.

Please note that this script was written with specific assumptions about the target website and may require customization if used for other websites.

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- Python (version 3.x)
- Selenium library (install using `pip install selenium`)
- Pillow library (install using `pip install pillow`)
- img2pdf library (install using `pip install img2pdf`)
- requests library (install using `pip install requests`)
- Microsoft Edge WebDriver (download the appropriate version for your Edge browser and specify the path in the script)

Or
- requirements.txt (install using `pip install -r requirements.txt`)
## How to Use

1. Clone this repository or copy the script to your local machine.
2. Make sure you have fulfilled the prerequisites mentioned above.
3. Set the `url` variable in the script to the URL of the specific chapter you want to download images from.
4. Set the path for the Edge WebDriver (`executable_path`) to the correct location on your machine.
5. Run the script using the Python interpreter.

Please ensure that you comply with the website's terms of service and avoid excessive scraping to avoid any legal issues.

## Script Workflow

1. The script loads the target URL and scrolls down to load all available chapters.
2. It extracts the chapter URLs and their corresponding titles and stores them in a dictionary.
3. Starting from the specified chapter (`start_compare`), the script loops through each chapter:
   - It opens the chapter URL and clicks on the reader area to reveal the images.
   - It downloads each image and converts it to JPG format.
   - It scrolls to each image's position on the page and captures a screenshot to convert to a PDF file.
   - It merges all the PDF files of a chapter into a single PDF file.
   - It repeats this process for subsequent chapters until it encounters a chapter with a number lower than the specified `start_compare`, at which point the script exits.


## Contact
- Discord : shiii#5276
