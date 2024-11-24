import os, requests, re

from urllib.parse import urlparse
from tqdm.asyncio import tqdm
from modules.services.ai import ai_parse
from modules.utils.validators import is_valid_image
from modules.utils.extract_it_id import extract_it_id
from modules.utils.parsers import parse_images
from modules.scrappers.fetch_page_source import fetch_page_source
from .fetch_page_source import fetch_page_source
from modules.utils.extract_it_id import extract_it_id
from playwright.async_api import async_playwright
import os
from urllib.parse import urlparse
import os


async def save_image(page, img_url, folder_path, idx):
    """이미지 URL에서 이미지를 다운로드하고 저장합니다."""
    try:
        # 특정 URL로 이동
        await page.goto(img_url)

        # 스크린샷 데이터를 변수에 저장
        screenshot_data = await page.screenshot()

        # 파일 이름 및 확장자 설정
        parsed_url = urlparse(img_url)
        file_name, file_extension = os.path.splitext(os.path.basename(parsed_url.path))

        if not file_extension:
            file_extension = ".jpg"

        img_path = os.path.join(folder_path, f"{idx}{file_extension}")

        # 이미지 저장
        with open(img_path, "wb") as file:
            file.write(screenshot_data)

        return img_path  # 저장된 이미지 경로 반환
    except Exception as e:
        print(f"이미지 저장 실패: {e}")
        return None


async def download_images(img_urls, folder_name):
    folder_path = os.path.join(f"이미지/{folder_name}", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    if not img_urls:
        return None

    saved_img_thumb_path = ""
    async with async_playwright() as playwright:
        driavers_path = os.path.join(os.getcwd(), "drivers")

        browser_path = os.path.join(
            driavers_path,
            "ms-playwright",
            "chromium-1140",
            "chrome-win",
            "chrome.exe",
        )

        browser = await playwright.chromium.launch(
            headless=False, executable_path=browser_path
        )

        context = await browser.new_context()
        await context.set_extra_http_headers(
            {
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
            }
        )
        page = await context.new_page()

        try:
            for idx, img_url in enumerate(
                tqdm(img_urls, desc="이미지 다운로드 중...", ascii=True, leave=False)
            ):
                if not img_url:
                    continue

                # 이미지 저장
                img_path = await save_image(page, img_url, folder_path, idx)
                if idx == 0 and img_path:
                    saved_img_thumb_path = img_path

        finally:
            await page.close()
            await context.close()
            await browser.close()
            return saved_img_thumb_path
