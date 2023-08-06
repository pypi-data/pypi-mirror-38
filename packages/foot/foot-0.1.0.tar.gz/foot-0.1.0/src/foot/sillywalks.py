import json
import os

from bs4 import BeautifulSoup


def walk(url, data, recursive=False):
    print(f"Walking: {url}")
    url_parts = url.split("/")[0:3]
    url_root = f"{url_parts[0]}//{url_parts[2]}"
    subdomain = url_parts[2]
    soup = BeautifulSoup(data["html"], "html.parser")
    href_links = []
    script_src = []
    page_refs = []
    for href in soup.find_all("a"):
        link = href.get("href")
        if "http" not in link:
            link = f"{url_root}{link}"
        href_links.append(link)
        if url_root in link:
            page_refs.append(link)
    for src in soup.find_all("script"):
        link = src.get("src")
        if "http" not in link:
            link = f"{url_root}{link}"
        script_src.append(link)

    result = {
        "url": url,
        "subdomain": subdomain,
        "status": data["status"],
        "headers": data["headers"],
        "cookies": data["cookies"],
        "title": soup.title.text,
        "links": href_links,
        "scripts": script_src,
    }

    create_file(result)

    if recursive:
        return page_refs
    else:
        return None


def create_file(results):
    if not os.path.exists("./foot"):
        os.makedirs("./foot")

    url_filename = results["url"].replace("/", "_").replace(".", "_").replace(":", "")
    with open(f"./foot/{url_filename}.json", "w") as json_file:
        json.dump(results, json_file)
