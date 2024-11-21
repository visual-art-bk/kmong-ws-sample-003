from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import io
import sys
import os, asyncio, urllib.parse, json
import google.generativeai as genai
from datetime import datetime
from tqdm.asyncio import tqdm
import nodriver as uc
import absl.logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from modules.utils.file_utils import read_urls, make_excel
from modules.scrappers import download_images

async def process_new_urls(urls: list, timestamp,  results, lock, model):
    for url in tqdm(urls, desc=f"총 {urls.__len__()}개 링크 순회 중...", ascii=True):
        folder_name = datetime.now().strftime(timestamp)

        async with lock:
            results[urllib.parse.unquote(url)] = {
                "결과": "",
                # "링크": urllib.parse.unquote(url),
                # "상품넘버": str(folder_name),
                "상품넘버": (
                    f'=HYPERLINK("{str(urllib.parse.unquote(url))}", "{str(folder_name)}")'
                ),
                "거래처": "",
                "단가": "",
                "이미지": "",
                "1차": "",
                "2차": "",
                "3차": "",
                "4차": "",
                "필터": "",
                "성별": "",
                "브랜드": "",
                "2차 브랜드": "",
                "상품명": "",
                "영문명": "",
                "추가 정보\n모델명": "",
                "추가 정보\n배송방법": "항공특송",
                "추가 정보\n소재": "",
                "추가 정보\n구성품": "풀박스",
                "매장가": "",
                "판매가1": "",
                "판매가2": "",
                "판매가3": "",
                "필수옵션\n등급선택": "",
                "필수옵션\n사이즈": "",
                "필수옵션\n색상": "",
                "필수옵션\n굽높이": "",
                "필수옵션\n버클": "",
                "필수옵션\n도금방식": "",
                "필수옵션\n밴드": "",
            }

        await download_images(
            url=urllib.parse.unquote(url),
            folder_name=str(folder_name),
            lock=lock,
            model=model,
            results=results,
        )
