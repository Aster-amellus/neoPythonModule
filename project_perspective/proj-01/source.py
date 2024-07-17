import requests
from lxml import etree

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
}

def get_video_cover(url: str) -> str:
    with requests.get(url, headers=HEADERS, timeout=10) as resp:
        resp.raise_for_status()
        source = resp.text

    html = etree.fromstring(
        source, parser=etree.HTMLParser()
    )
    xpath = '//meta[@itemprop="image"]'
    element = html.xpath(xpath)[0]
    cover_url = element.attrib.get("content")

    return "https:" + cover_url.split("@")[0]

def main():
    url = input("Input your video URL:").strip()
    cover = get_video_cover(url)
    print("Cover URL:", cover)

if __name__ == "__main__":
    main()
