import os, requests, re

from urllib.parse import urlparse
from tqdm.asyncio import tqdm
from modules.services.ai import ai_parse
from modules.utils.validators import is_valid_image
from modules.utils.extractors import extract_it_id
from modules.utils.parsers import parse_images
from modules.scrappers.fetch_page_source import fetch_page_source
from .fetch_page_source import fetch_page_source
from modules.utils.extractors import extract_it_id


async def download_images(url, folder_name, lock, results, model):
    item_id = extract_it_id(url)

    folder_path = os.path.join(f"이미지/{item_id}", folder_name)

    os.makedirs(folder_path, exist_ok=True)

    html_data = await fetch_page_source(
        lock=lock, url=url, results=results, folder_path=folder_path
    )

    img_urls = parse_images(html_data, url)

    thumb_path = ""
    if len(img_urls) > 0:
        idx = 0
        for img_url in tqdm(img_urls, desc="이미지 다운로드 중...",  ascii=True, leave=False):
            if img_url == "":
                continue

            headers = {
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
            }
            try:
                img_response = requests.get(
                    img_url, headers=headers, stream=True, timeout=120
                )
                img_response.raise_for_status()
            except Exception:
                continue

            if not is_valid_image(img_response.content):
                continue

            parsed_url = urlparse(img_url)
            file_name, file_extension = os.path.splitext(
                os.path.basename(parsed_url.path)
            )

            if not file_extension:
                file_extension = ".jpg"

            img_path = os.path.join(folder_path, f"{item_id}_{idx}{file_extension}")

            with open(img_path, "wb") as file:
                for chunk in img_response.iter_content(1024):
                    file.write(chunk)

            if idx == 0:
                thumb_path = img_path

            idx += 1

        async with lock:
            results[url]["결과"] = "성공"
            results[url]["이미지"] = thumb_path

        try:
            parsed_data = ai_parse(ai_model=model, html_data=html_data)

            async with lock:
                results[url]["매장가"] = parsed_data["market_price"]
                results[url]["단가"] = parsed_data["price"]
                results[url]["성별"] = parsed_data["gender"]
                results[url]["상품명"] = (
                    re.match(r"^\[.*?\] (.*)", str(parsed_data["kor_name"])).group(1)
                    if re.match(r"^\[.*?\] (.*)", str(parsed_data["kor_name"]))
                    else str(parsed_data["kor_name"])
                )
                results[url]["영문명"] = (
                    re.match(r"^\[.*?\] (.*)", str(parsed_data["eng_name"])).group(1)
                    if re.match(r"^\[.*?\] (.*)", str(parsed_data["eng_name"]))
                    else str(parsed_data["eng_name"])
                )
                results[url]["브랜드"] = parsed_data["brand"].upper()
                results[url]["2차"] = parsed_data["first_category"]
                results[url]["3차"] = parsed_data["second_category"]
                results[url]["추가 정보\n모델명"] = str(parsed_data["genuine_number"])
                results[url]["필수옵션\n색상"] = ",".join(parsed_data["colors"])
                results[url]["필수옵션\n사이즈"] = (
                    ",".join(parsed_data["sizes"]).replace("(", "[").replace(")", "]")
                )
        except Exception:
            async with lock:
                results[url]["결과"] = "실패"
    else:
        async with lock:
            results[url]["결과"] = "실패"
