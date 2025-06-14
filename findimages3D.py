import os
import requests
import time
from tqdm import tqdm
import zipfile
import shutil

# CONFIGURATION
API_TOKEN = "f0c963db748742feb6fde1f20db8b517"  # replace with your actual token
DOWNLOAD_DIR = "static/assets/3d/"
QUERY = "india"
MAX_MODELS = 5

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

SEARCH_URL = "https://api.sketchfab.com/v3/search"
DOWNLOAD_URL_TEMPLATE = "https://api.sketchfab.com/v3/models/{}/download"
headers = { "Authorization": f"Token {API_TOKEN}" }

def validate_token():
    response = requests.get("https://api.sketchfab.com/v3/me", headers=headers)
    if response.status_code == 200:
        print("✅ Token is valid.")
    else:
        print("❌ Invalid token.")
        exit(1)

def search_models():
    results = []
    page = 1
    per_page = min(MAX_MODELS, 24)

    while len(results) < MAX_MODELS:
        params = {
            "type": "models",
            "downloadable": "true",
            "license": "cc0",
            "q": QUERY,
            "sort_by": "relevance",
            "per_page": per_page,
            "page": page
        }
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        models = response.json().get("results", [])
        if not models: break
        results.extend(models)
        if len(models) < per_page: break
        page += 1

    return results[:MAX_MODELS]

def download_model(model):
    uid = model["uid"]
    name = model["name"].replace("/", "_").replace("\\", "_")
    download_url = DOWNLOAD_URL_TEMPLATE.format(uid)

    response = requests.get(download_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get download URL for model {name}")
        return None

    gltf_info = response.json().get("gltf", None)
    if not gltf_info:
        print(f"No glTF version for model {name}")
        return None

    model_url = gltf_info["url"]
    file_path = os.path.join(DOWNLOAD_DIR, f"{uid}.zip")

    with requests.get(model_url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with open(file_path, 'wb') as f, tqdm(
            desc=name, total=total_size, unit='iB', unit_scale=True
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

    print(f"✅ Downloaded {name} to {file_path}")
    return uid, file_path

def extract_gltf(uid, zip_path):
    extract_dir = os.path.join(DOWNLOAD_DIR, uid)
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    os.remove(zip_path)
    print(f"✅ Extracted to {extract_dir}")

def main():
    validate_token()
    models = search_models()
    print(f"Found {len(models)} models")
    for model in models:
        uid, zip_file = download_model(model)
        if zip_file:
            extract_gltf(uid, zip_file)
            time.sleep(1)

if __name__ == "__main__":
    main()
