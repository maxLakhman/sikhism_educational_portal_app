import requests
import os
import re
import json

# URL of the plain text file
URL = "https://www.gutenberg.org/ebooks/53510"
OUTPUT_FILE = "data/sikhism_cleaned.jsonl"
os.makedirs("data", exist_ok=True)

def clean_text(text):
    # Remove Gutenberg license and boilerplate
    start = re.search(r"\*\*\* START OF.*?\*\*\*", text)
    end = re.search(r"\*\*\* END OF.*?\*\*\*", text)
    if start and end:
        text = text[start.end():end.start()]
    return text.strip()

def main():
    print("Downloading...")
    res = requests.get(URL)
    raw_text = res.text

    print("Cleaning...")
    cleaned = clean_text(raw_text)

    print("Saving...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for paragraph in cleaned.split("\n\n"):
            f.write(json.dumps({"text": paragraph.strip()}) + "\n")

    print(f"✅ Done. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
