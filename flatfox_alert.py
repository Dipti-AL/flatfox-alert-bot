import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://flatfox.ch/en/regimo-zug/listings"
SEEN_FILE = "seen.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen(ids):
    with open(SEEN_FILE, "w") as f:
        json.dump(ids, f)

def fetch_listings():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("a[href^='/en/regimo-zug/listing/']")

    listings = []
    for card in cards:
        href = card.get("href")
        id = href.split("/")[-2]
        title = card.get_text(strip=True)
        listings.append({"id": id, "title": title, "url": "https://flatfox.ch" + href})
    return listings

def main():
    seen_ids = load_seen()
    new_listings = []
    listings = fetch_listings()

    for l in listings:
        if l["id"] not in seen_ids:
            new_listings.append(l)

    if new_listings:
        print(f"🔔 Found {len(new_listings)} new listings:")
        for l in new_listings:
            print(f"{l['title']} → {l['url']}")
        seen_ids += [l["id"] for l in new_listings]
        save_seen(seen_ids)
    else:
        print("No new listings.")

if __name__ == "__main__":
    main()
