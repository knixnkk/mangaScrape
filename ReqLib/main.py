import requests
import re
import json
from bs4 import BeautifulSoup
from mics import concat, get_all_files_in_folder, merge_pdfs
import os
import requests
from PIL import Image
import img2pdf
from PIL import Image
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from io import BytesIO
from fake_useragent import UserAgent
from pathlib import Path
import json
import asyncio
import aiohttp
import time

def readJson():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data
def writeJson(data):
    with open('config.json', "w") as f:
        data = json.dump(data, f)

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
    with open(img_path, "rb") as image_file:
        image_data = image_file.read()
        pdf_bytes = img2pdf.convert(image_data)
    
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(pdf_bytes)

def convert_images_to_pdfs(image_files, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with ThreadPoolExecutor() as executor:
        future_to_pdf = {executor.submit(imgtopdf, img_path, os.path.join(output_folder, f"{os.path.splitext(os.path.basename(img_path))[0]}.pdf")): img_path for img_path in image_files}

        for future in as_completed(future_to_pdf):
            img_path = future_to_pdf[future]
            try:
                future.result()
            except Exception as exc:
                print(f"Conversion for '{img_path}' raised an exception: {exc}")

MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds

async def download_and_convert_image(image_url, save_path):
    for retry in range(MAX_RETRIES + 1):
        try:
            ua = UserAgent()
            headers = {'User-Agent': ua.random}

            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(image_url, timeout=60) as response:
                    response.raise_for_status()
                    image_content = await response.read()

            with Image.open(BytesIO(image_content)) as img:
                img = img.convert("RGB")
                img.save(save_path, "JPEG")

            input_text = f"[ download_and_convert_image ] : Image downloaded and saved as {save_path}"
            break  # Break out of retry loop if successful
        except asyncio.TimeoutError:
            if retry < MAX_RETRIES:
                print(f"Timeout occurred for image {image_url}. Retrying...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                input_text = f"[ download_and_convert_image ] : Max retries reached for image {image_url}."
        except (aiohttp.ClientError, OSError) as e:
            input_text = f"[ download_and_convert_image ] : Error for image {image_url}: {e}"

    gradient_result = generate_gradient(input_text)
    print(gradient_result)
async def download_and_convert_images(img_src):
    tasks = []
    for file_name, image_url in img_src.items():
        save_path = f"images/{file_name}.jpg"
        task = asyncio.create_task(download_and_convert_image(image_url, save_path))
        tasks.append(task)

    await asyncio.gather(*tasks)


start_time = time.time()
count_title = 0
while True:
    count_title += 1
    url = readJson()['url']
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tags = soup.find_all('script')


    target_script = None
    provided_js_script = None
    for script in script_tags:
        if script.string:
            if 'ts_reader.run' in script.string:
                target_script = script
            elif 'HISTORY.push' in script.string:
                provided_js_script = script

    if target_script is not None:
        # Extracting the JSON data from the script using regex
        pattern = r'ts_reader\.run\((.*)\);'
        match = re.search(pattern, target_script.string, re.DOTALL)

        if match:
            json_data = match.group(1)

            # Parsing the JSON data
            parsed_data = json.loads(json_data)

            # Accessing the values of prevUrl, nextUrl, and images
            prev_url = parsed_data['prevUrl']
            next_url = parsed_data['nextUrl']
            images = parsed_data['sources'][0]['images']
            div_tag = soup.find('div', class_='daw chpnw')
            a_tag = soup.find('a', itemprop='item')
            if a_tag:
                text = a_tag.text.strip()
                print(text)
            else:
                print("The specified <a> tag with itemprop='item' not found.")
            if div_tag:
                print(div_tag.text.strip())
            else:
                print("The specified div with class 'daw chpnw' not found.")
            images = {str(i + 1): url for i, url in enumerate(images)}
            print("nextUrl:", next_url)
            print("images:", images)
            url = next_url
            print('\n\n')
        else:
            print("JSON data not found in the script.")
    else:
        print("Function not found in any script tag.")
    if next_url == "":
        print("Break")
    if provided_js_script:
        chapter_title_match = re.search(r'"chapter_title":"([^"]+)"', provided_js_script.string)
        if chapter_title_match:
            chapter_title = chapter_title_match.group(1)
            chapter_title = chapter_title.encode().decode('unicode_escape')
            print("Chapter Title from provided JS script:", chapter_title)
        else:
            print("Chapter Title not found in the provided JS script.")
    else:
        print("Provided JS script not found.")
    allc_div = soup.find('div', class_='allc')

    if allc_div:
        link_element = allc_div.find('a')
        if link_element:
            text_inside_a = link_element.get_text()
            print(text_inside_a)
        else:
            print("No <a> element found inside the <div class='allc'> element.")
    else:
        print("The <div class='allc'> element was not found.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_and_convert_images(images))
    image_files = get_all_files_in_folder("images/")
    output_folder = "pdf"
    input_text = f"Convert Image to pdf {image_files}"
    gradient_result = generate_gradient(input_text)
    print(gradient_result)
    convert_images_to_pdfs(image_files, output_folder)
    img_folder = get_all_files_in_folder("images/")
    input_text = f"Delete the original image {img_folder}"
    gradient_result = generate_gradient(input_text)
    print(gradient_result)
    for file_image in img_folder:
        os.remove(file_image)
    input_folder = "pdf/"
    merge_pdfs(input_folder, f"chapter/{count_title}.pdf")
    if next_url == '':
        break
    else:
        writeJson(
            {
                "url" : str(next_url)
            }
        )
if not os.path.exists(f"store/{text_inside_a}"):
    os.makedirs(f"store/{text_inside_a}")

move_files = get_all_files_in_folder('chapter/')
for move_file in move_files:
    text = move_file
    replaced = text.replace("chapter/", f"store/{text_inside_a.rstrip()}/")
    src_file = Path(text)

    dst_file = Path(replaced)

    src_file.rename(dst_file)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")