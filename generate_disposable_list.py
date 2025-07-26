import requests

DISPOSABLE_LIST_URL = "https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/master/domains.txt"
OUTPUT_FILE = "disposable_domains.txt"

def download_disposable_domains():
    print("Downloading disposable domain list...")
    response = requests.get(DISPOSABLE_LIST_URL)
    if response.status_code == 200:
        with open(OUTPUT_FILE, "w") as f:
            f.write(response.text)
        print(f"✅ Saved {len(response.text.splitlines())} domains to {OUTPUT_FILE}")
    else:
        print(f"❌ Failed to download list. Status code: {response.status_code}")

if __name__ == "__main__":
    download_disposable_domains()