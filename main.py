import bs4
import requests
import os

from typing import Optional


base_url = "https://pycon-2024.python.ph"

def create_directory(file_path: Optional[str] = None):
    if file_path is None:
        return

    directories = file_path.split("/")
    directory_path = ""
    for dir in directories:
        if not dir:
            continue

        if "." in dir:
            # TODO: Improve filetype checking
            continue

        if directory_path:
            directory_path += f"/{dir}"
            continue

        directory_path = dir
    else:
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)


def download_and_write_files(source, decoded=False):
    create_directory(source)
    response = requests.get(f"{base_url}{source}")

    with open(source[1:], "w" if not decoded else "wb") as assets:
        content = response.text

        if decoded:
            content = response.content

        assets.write(content)
        print(source)
        print("File written!")


def replace_source(element: bs4.element.Tag):
    attribute_map = {
        "link": "href",
        "script": "src",
        "img": "src",
    }

    if not isinstance(element, bs4.element.Tag):
        return

    el_name = element.name
    if el_name not in ("link", "script", "img"):
        return

    source = element.attrs.get("href") or element.attrs.get("src")
    if not source:
        return

    download_and_write_files(source, decoded=el_name=="img")
    attr = attribute_map[el_name]
    element[attr] = source[1:]


def find_and_replace(source):

    output_files = ["index.html", "static/CACHE/css/output.0d0b7f46a680.css"]

    for path in output_files:
        with open(path, "r") as index:
            updated = index.read().replace(source, source[1:])

        with open(path, "w") as index:
            index.write(updated)


def download_404_files():
    style_files = [
        "/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js",
        "/static/fonts/Fira-Sans/Fira-Sans-Regular.979a13914c33.woff2?7520f715b682",
        "/static/fonts/Fira-Sans/Fira-Sans-Regular.200d5e7cc951.woff?7520f715b682",
        "/static/fonts/Fira-Sans-Condensed/Fira-Sans-Condensed-Regular.a6ce9bccb82f.ttf?7520f715b682",
        "/static/fonts/Fira-Sans-Condensed/Fira-Sans-Condensed-Medium.7ebb6cc036e2.ttf?7520f715b682",
        "/static/fonts/Baybayin-Sisil/Baybayin-Sisil.3c00ff59de73.ttf?7520f715b682",
        "/static/img/bg/bg-1.d99092a240c9.jpg?7520f715b682",
        "/static/img/function/ayala.54532653b915.jpg",
        "/static/img/function/magallanes.280fc78565b2.jpg",
        "/static/img/function/belair.cd7b9faa35f1.jpg",
        "/static/img/bg/bg-2.484d629ca940.jpg?7520f715b682",
        "/static/img/bg/bg-3.65dc74019c1c.jpg?7520f715b682",
    ]

    for source in style_files:
        decoded = ".jpg" in source
        download_and_write_files(source, decoded)
        find_and_replace(source)


def get_page():
    page = requests.get(base_url)

    soup = bs4.BeautifulSoup(page.text, features="html.parser")
    for element in soup.head:
        replace_source(element)

    for element in soup.html.body:
        replace_source(element)

    for element in soup.find_all("img"):
        replace_source(element)

    # Save the page to index.html
    with open("index.html", "w") as file:
        file.write(str(soup.html))

    download_404_files()

if __name__ == "__main__":
    get_page()
