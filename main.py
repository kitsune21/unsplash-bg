from dotenv import load_dotenv
from save_image import *
from set_background import *
import os
import requests

load_dotenv()

api_key = os.environ.get("UNSPLASH_KEY")
api_base_url = "https://api.unsplash.com"
get_random = "/photos/random/?orientation=landscape"
client_key = "&client_id=" + api_key

def get_random_picture():
  res = requests.get(api_base_url + get_random + client_key)
  if res.status_code != 200:
    print(f"Error: {res.text}")
    return
  return res.json()

def download_image(image_url, file_name):
  path = get_default_backgrounds_directory() + f"/{file_name}"
  try:
    response = requests.get(image_url, stream=True)

    response.raise_for_status()

    with open(path, 'wb') as f:
      for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
    print(f"Image downloaded to {path}")
    return path
  except requests.exceptions.RequestException as e:
    print(f"Error downloading image: {e}")
  except IOError as e:
    print(f"Error saving image to file: {e}")
  

if __name__ == "__main__":
  image_data = get_random_picture()
  image_full_path = download_image(image_data["urls"]["raw"], f"{image_data["slug"]}.png")
  set_desktop_wallpaper(image_full_path)
