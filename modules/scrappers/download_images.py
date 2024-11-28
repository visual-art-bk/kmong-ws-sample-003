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
from modules.utils.wrap_browser_page import WsBrowser
from modules.utils.Logger import Logger


async def save_image(img_url, folder_path, idx):

    async with async_playwright() as playwright:
        async with WsBrowser(playwright=playwright) as ws_browser:
            try:
                # 특정 URL로 이동
                await ws_browser.goto(img_url)

                # 스크린샷 데이터를 변수에 저장
                screenshot_data = await ws_browser.page.screenshot()

                # 파일 이름 및 확장자 설정
                parsed_url = urlparse(img_url)
                file_name, file_extension = os.path.splitext(
                    os.path.basename(parsed_url.path)
                )

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


def should_skip_image(img_url, no_down_imgs_prefix):
    # any()를 사용하여 URL에 제외 키워드가 포함되어 있는지 확인
    return any(no_down_img in img_url for no_down_img in no_down_imgs_prefix)


async def download_images(img_urls, folder_name):
    logger = Logger(log_file="logs/ws/dw/exc.log", name="save_image").get_logger()
    folder_path = os.path.join(f"이미지/{folder_name}", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    if not img_urls:
        return None

    saved_img_thumb_path = ""

    # "inipay" 이니페이 썸네일
    no_down_imgs_prefix = ["kakao", "btn", "close", "inipay"]

    try:
        done_thum_in_excel = False

        for idx, img_url in enumerate(
            tqdm(img_urls, desc="이미지 다운로드 중...", ascii=True, leave=False)
        ):
            if not img_url or should_skip_image(img_url, no_down_imgs_prefix):
                logger.info(f"이미지 다운링크 {img_url} 스킵\n")
                continue

            # 이미지 저장
            img_path = await save_image(img_url, folder_path, idx)
            logger.info(f"이미지 다운링크 {img_url} 저장성공\n")

            if idx == 0 and img_path:
                saved_img_thumb_path = img_path

                done_thum_in_excel = True

                continue

            elif done_thum_in_excel == False and not idx == 0 and img_path:
                saved_img_thumb_path = img_path

                done_thum_in_excel = True
                continue

    finally:
        if done_thum_in_excel == False:
            saved_img_thumb_path = ""

        return saved_img_thumb_path
