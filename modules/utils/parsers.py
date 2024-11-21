from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_images(html_data, url):
    soup = BeautifulSoup(html_data, "html.parser")

    for tag in soup.find_all(["header", "head", "footer"]):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "recommend" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "relate" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "logo" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "together" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "list" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "review" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "banner" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "category" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "option" in class_name
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=lambda class_name: class_name and "guide" in class_name
    ):
        tag.decompose()

    img_tags = soup.find_all("img")
    img_urls = [
        (
            urljoin(url, img["src"])
            if ";base64," not in img["src"]
            else (
                urljoin(url, img["ec-data-src"]) if "ec-data-src" in img.attrs else ""
            )
        )
        for img in img_tags
        if "src" in img.attrs
        and not img["src"].lower().endswith(".svg")
        and not "//img.echosting.cafe24.com/" in img["src"]
        and "/theme/" not in img["src"]
        and "facebook" not in img["src"]
        and "icon" not in img["src"]
        and "logo" not in img["src"]
        and "common" not in img["src"]
        and "banner" not in img["src"]
        and "brand" not in img["src"]
    ]

    return img_urls
