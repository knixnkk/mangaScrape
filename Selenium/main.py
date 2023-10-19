from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from mics import concat, get_all_files_in_folder, merge_pdfs
import os
from selenium.webdriver.support.ui import Select
import requests
from PIL import Image
import img2pdf
from PIL import Image
import concurrent.futures
import colorama
import random
from io import BytesIO
from pathlib import Path
import psutil
import json
import asyncio
import aiohttp
colorama.init(autoreset=True)
max_retries = 20
retries = 0

def readJson():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data
def writeJson(data):
    with open('config.json', "w") as f:
        data = json.dump(data, f)
        
def is_msedge_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'msedge.exe':
            return True
    return False

def generate_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def generate_gradient(text):
    start_color = generate_random_color()
    end_color = generate_random_color()
    num_chars = len(text)
    color_diff = [(end - start) / num_chars for start, end in zip(start_color, end_color)]
    gradient_text = ""

    for i, char in enumerate(text):
        r = start_color[0] + int(color_diff[0] * i)
        g = start_color[1] + int(color_diff[1] * i)
        b = start_color[2] + int(color_diff[2] * i)
        gradient_text += f"\033[38;2;{r};{g};{b}m{char}\033[0m"

    return gradient_text

def imgtopdf(img_path, pdf_path):
    image = Image.open(img_path)
    pdf_bytes = img2pdf.convert(image.filename)
    image.close()
    
    with open(pdf_path, "wb") as file:
        file.write(pdf_bytes)
    

def convert_images_to_pdfs(image_files, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(imgtopdf, img_path, os.path.join(output_folder, f"{os.path.splitext(os.path.basename(img_path))[0]}.pdf")) for img_path in image_files]
        concurrent.futures.wait(futures)
async def download_and_convert_image(image_url, save_path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                response.raise_for_status()
                image_content = await response.read()

        with Image.open(BytesIO(image_content)) as img:
            img = img.convert("RGB")
            img.save(save_path, "JPEG")

        input_text = f"[ download_and_convert_image ] : Image downloaded and saved as {save_path}"
    except aiohttp.ClientError as e:
        input_text = f"[ download_and_convert_image ] : Error downloading image: {e}"
    except OSError as e:
        input_text = f"[ download_and_convert_image ] : Error converting image: {e}"

    os.system(f'title {name_chapter} : {save_path}')
    gradient_result = generate_gradient(input_text)
    print(gradient_result)
async def download_and_convert_images(img_src):
    tasks = []
    for file_name, image_url in img_src.items():
        save_path = f"images/{file_name}.jpg"
        task = asyncio.create_task(download_and_convert_image(image_url, save_path))
        tasks.append(task)

    await asyncio.gather(*tasks)
def scroll_to_position(x, y):
    driver.execute_script(f"window.scrollTo({x}, {y});")

def get_element_position(element):
    return element.location["x"], element.location["y"]
def slow_scroll_page_within_duration(driver, total_duration=30, num_scrolls=10):
    scroll_amount = 200  
    scroll_delay = total_duration / (2 * num_scrolls)

    actions = ActionChains(driver)

    num_scrolls_per_direction = num_scrolls // 2
    x_choice = random.choice(["Up","Down"])
    if x_choice == "Down":
        for _ in range(num_scrolls_per_direction):
            actions.send_keys(Keys.ARROW_DOWN)
            actions.perform()
            for _ in range(20):
                driver.execute_script('window.scrollBy(0,100)')
                sleep(0.1)
            sleep(scroll_delay)
    else:
        for _ in range(num_scrolls_per_direction):
            actions.send_keys(Keys.ARROW_UP)
            actions.perform()
            for _ in range(20):
                driver.execute_script('window.scrollBy(0,-100)')
                sleep(0.1)
            sleep(scroll_delay)
    sleep(2)
def checkImgExtension():
    readarea_element = driver.find_element_by_css_selector("#readerarea")
    img_elements = readarea_element.find_elements(By.TAG_NAME, "img")
    page_number = [page_src.get_attribute("src") for page_src in img_elements]
    count = 0
    img_src = []
    for n_src in page_number:
        extension = n_src.split(".")[-1]
        if extension == "png" or extension == "jpg" or extension == "webp":
            count += 1
            img_src.append(n_src)
    img_src = {str(i + 1): url for i, url in enumerate(img_src)}
    return count, img_src , len(page_number)


url = readJson()['url']
start_compare = url.split('-')[-1].rstrip('/')

driver = webdriver.Edge(executable_path=r'C:\Path\msedgedriver.exe')

while retries < max_retries:
    try:

        driver.get(url)
        slow_scroll_page_within_duration(driver, total_duration=30, num_scrolls=10)
        for _ in range(20):
            driver.execute_script('window.scrollBy(0,100)')
            sleep(0.1)
        sleep(1)
        Chapter_element = driver.find_element(By.CSS_SELECTOR, "#chapter")
        options = Chapter_element.find_elements(By.TAG_NAME, "option")
        title = driver.title
        select_data = []
        option_values = []
        for option in options:
            text = option.text
            val = option.get_attribute("value")
            if text != "Select Chapter":
                select_data.append(text)
            if val != "":
                option_values.append(val)

        chapter = concat(select_data, option_values)
        reversed_chapters = dict(reversed(chapter.items()))
        gradient_result = generate_gradient(reversed_chapters)
        print(gradient_result)
        driver.quit()
        for name_chapter, v in reversed_chapters.items():
            print(name_chapter, v)
            name_chapter = name_chapter.rstrip(' [รออัพเดท]')
            name_chapter = name_chapter.rstrip(' [รออัปเดต]')
            print(f"{name_chapter}/{len(reversed_chapters)}")
            end_compare = name_chapter.split(' ')[-1]
            if int(end_compare) >= int(start_compare):
                os.system(f'title {name_chapter}')
                driver = webdriver.Edge(executable_path=r'C:\Path\msedgedriver.exe')
                os.system('cls')
                driver.get(v)
                input_text = v
                os.system(f'title {name_chapter} : "Open Website"')
                gradient_result = generate_gradient(input_text)
                print(gradient_result)
                try:
                    driver.execute_script('document.querySelector(\'a[href="javascript:void(0)"]\').click();')
                except:
                    pass
                input_text = (f"COMPARED : {end_compare} and {start_compare}")
                gradient_result = generate_gradient(input_text)
                print(gradient_result)
                
                
                n_count, img_src, n_page = checkImgExtension()
                print(f"n_count {n_count}, n_page {n_page}, img_src {img_src}")
                select_element = driver.find_element_by_css_selector("#select-paged")
                options = select_element.find_elements(By.TAG_NAME, "option")
                option_values = [option.get_attribute("value") for option in options]
                gradient_result = generate_gradient(option_values)
                print(gradient_result)
                os.system(f'title {name_chapter} : {len(option_values)}')
                for i in range(2):
                    select = Select(select_element)
                    for value in option_values:
                        select.select_by_value(value)
                        sleep(1)
                file_name_count = 0
                while True:
                    n_count, img_src, n_page = checkImgExtension()
                    print(f"n_count {n_count}, n_page {n_page}, img_src {img_src}")
                    if n_count == n_page == len(img_src):
                        os.system('cls')
                        print("DOWNLOAD")
                        print(f"n_count {n_count}, n_page {n_page}, img_src {img_src}")
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(download_and_convert_images(img_src))
                        sleep(2)
                        image_files = get_all_files_in_folder("images/")
                        output_folder = "pdf"
                        input_text = f"Convert Image to pdf {image_files}"
                        os.system(f'title {name_chapter} : {input_text}')
                        gradient_result = generate_gradient(input_text)
                        print(gradient_result)
                        convert_images_to_pdfs(image_files, output_folder)
                        sleep(1)
                        img_folder = get_all_files_in_folder("images/")
                        input_text = f"Delete the original image {img_folder}"
                        os.system(f'title {name_chapter} : {input_text}')
                        gradient_result = generate_gradient(input_text)
                        print(gradient_result)
                        for file_image in img_folder:
                            os.remove(file_image)
                        sleep(1)
                        input_folder = "pdf/"
                        input_text = f"Merge pdf {name_chapter}"
                        os.system(f'title {name_chapter} : {input_text}')
                        gradient_result = generate_gradient(input_text)
                        print(gradient_result)
                        merge_pdfs(input_folder, f"chapter/{name_chapter}.pdf")
                        All_chapter_element = driver.find_element(By.CLASS_NAME, 'allc')
                        title_element = All_chapter_element.find_element(By.TAG_NAME, "a")
                        chap = title_element.text
                        print(chap)
                        break
                    else:
                        total_dur = random.randint(30,60)
                        num_scr = random.randint(10,40)
                        slow_scroll_page_within_duration(driver, total_duration=total_dur, num_scrolls=num_scr)
                        select_element = driver.find_element_by_css_selector("#select-paged")
                        options = select_element.find_elements(By.TAG_NAME, "option")
                        option_values = [option.get_attribute("value") for option in options]
                        gradient_result = generate_gradient(option_values)
                        print(gradient_result)
                        os.system(f'title {name_chapter} : {len(option_values)}')
                        select = Select(select_element)
                        for value in option_values:
                            select.select_by_value(value)
                            sleep(1)
                            
                sleep(5)
                writeJson(
                    {
                        "url" : str(v)
                    }
                )
                driver.quit()
        if not os.path.exists(f"store/{chap}"):
            os.makedirs(f"store/{chap}")

        move_files = get_all_files_in_folder('chapter/')
        for move_file in move_files:
            text = move_file
            replaced = text.replace("chapter/", f"store/{chap.rstrip()}/")
            src_file = Path(text)

            dst_file = Path(replaced)

            src_file.rename(dst_file)
    except Exception as e:
            # Print the error message
            print(f"Error occurred: {e}")

            # Increase the number of retries
            retries += 1

            # Wait for a few seconds before the next attempt (optional)
            sleep(5)

# If the loop completes all retries without success, print a message
if retries == max_retries:
    print("Maximum number of retries reached. Script could not complete successfully.")