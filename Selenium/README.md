# Selenium Version


_This Python script uses Selenium to download and convert images from a web page to PDF. It first opens the web page in Microsoft Edge and scrolls to the bottom of the page. Then, it finds all of the images on the page and downloads them to a folder called `images`. Finally, it converts the images to PDF and saves them to a folder called `pdf`._

The script also uses a few other Python libraries, including:

 - `concurrent.futures`: This library allows the script to run multiple tasks concurrently, which can improve performance.
 - `colorama`: This library allows the script to print colored text to the console.
 - `pathlib`: This library provides a high-level interface to the path system.
 - `psutil`: This library provides information about running processes.
 - `aiohttp`: This library is used to download the images asynchronously.
 - `img2pdf`: This library is used to convert the images to PDF.


Features:

 - Download images from a web page using Selenium
 - Convert images to PDF using img2pdf
 - Run multiple tasks concurrently to improve performance
 - Print colored text to the console for easier readability
 - Customize the output folder and maximum number of retries using a JSON configuration file

__Make a folder called chapter, images, pdf, store to get no error__
