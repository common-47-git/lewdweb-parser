import asyncio
import aiohttp
import aiofiles
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup as BS
import os

PATH_TO_SAVE = r"C:\Users\commo\OneDrive\Изображения\Saved Pictures\shiro"

async def download_image(url, save_path, i):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Response code
                response.raise_for_status()

                # Extracting the file extension from the URL and adding a default extension
                parsed_url = urlparse(url)
                file_extension = os.path.splitext(unquote(parsed_url.path))[1]
                if not file_extension:
                    file_extension = ".jpg"
                file_name = f"image_{i}{file_extension}"
                file_path = os.path.join(save_path, file_name)

                # Save the content of the response as an image file
                async with aiofiles.open(file_path, 'wb') as file:
                    await file.write(await response.read())
                print(f"Image downloaded and saved at: {file_path}")

    except aiohttp.ClientError as e:
        print(f"Error downloading the image: {e}")

async def main():
    base_url = 'https://forum.lewdweb.net'
    image_counter = 1

    for page_number in range(120):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://forum.lewdweb.net/threads/shirogane-sama.1071/page-{page_number}") as r:
                html = BS(await r.text(), 'html.parser')

        tasks = []
        for el in html.select(".file-preview"):
            end_url = base_url + el.get('href')
            file_path = os.path.join(PATH_TO_SAVE, f"image_{image_counter}.jpg")

            if os.path.exists(file_path):
                print(f"The file at {file_path} exists.")
            else:
                tasks.append(download_image(end_url, PATH_TO_SAVE, image_counter))
            image_counter += 1

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
