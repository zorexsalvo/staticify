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


def download_static_files(element: bs4.element.Tag):
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

    create_directory(source)
    response = requests.get(f"{base_url}{source}")

    with open(source[1:], "w") as css:
        css.write(response.text)

        attr = attribute_map[el_name]
        element[attr] = source[1:]
        print(element)
        print("File written!")


def get_page():
    page = requests.get(base_url)

    soup = bs4.BeautifulSoup(page.text, features="html.parser")
    for element in soup.head:
        download_static_files(element)

    for element in soup.html.body:
        download_static_files(element)

    for element in soup.find_all("img"):
        download_static_files(element)

    # Save the page to index.html
    with open("index.html", "w") as file:
        file.write(str(soup.html))


if __name__ == "__main__":
    get_page()
