import requests
from shutil import copyfileobj


def download_image_and_get_filename(url: str) -> str:
    response = requests.get(url, stream=True)
    filename = url.split("/")[-1]

    if response.status_code == 200:
        response.raw.decode_content = True
        with open(f'media/products/{filename}', 'wb') as f:
            copyfileobj(response.raw, f)

    return filename
