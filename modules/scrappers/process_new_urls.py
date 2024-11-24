import traceback
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import asyncio
from datetime import datetime
import urllib.parse
from .download_images import download_images
from .fetch_page_source import fetch_page_source
from modules.utils import parse_images
from modules.services.ai import ai_parse
from modules.utils import save_scraping_result
from modules.utils import extract_it_id


async def process_url(url, results, model):
    """
    주어진 URL에 대해 필요한 데이터를 생성하고 이미지를 다운로드합니다.
    """

    try:
        prod_id =  extract_it_id(url=url)

        folder_name = datetime.now().strftime("%Y%m%d%H%M%S")  # 폴더 이름 생성

        html_data = await fetch_page_source(folder_path=folder_name, url=url)

        if not html_data:
            results[url] = {"결과": "실패"}
            return

        img_urls = await parse_images(html_data=html_data, url=url)

        if len(img_urls) == 0:
            results[url] = {"결과": "실패"}
            return

        ai_parsed_data = await ai_parse(ai_model=model, html_data=html_data)

   

        saved_img_thumb_path = await download_images(
            folder_name=prod_id, img_urls=img_urls
        )

        if not saved_img_thumb_path:
            pass

        import os, requests, asyncio, urllib.parse, json, re
        from urllib.parse import urljoin, urlparse

        def get_img_path_for_excel(img_url, thumb_img_name, folder_path):
            parsed_url = urlparse(img_url)
            file_name, file_extension = os.path.splitext(
                os.path.basename(parsed_url.path)
            )

            if not file_extension:
                file_extension = ".jpg"

            img_path = os.path.join(folder_path, f"{thumb_img_name}{file_extension}")

            return img_path

        saved_img_thumb_path_2 = get_img_path_for_excel(
            folder_path=folder_name,
            img_url=img_urls[0],
            thumb_img_name=0,
        )

        scrapping_result = save_scraping_result(
            parsed_data=ai_parsed_data,
            thumb_path=saved_img_thumb_path,
            url=url,
            folder_name=folder_name,
        )

    except Exception as e:
        print(f"url 스크래핑 중 에러: {e}")
        print("TRACEBACK:")
        traceback.print_exc()  # 상세한 예외 정보 출력

    finally:
        if not scrapping_result:
            return {[url]: {}}
        return scrapping_result


async def process_new_urls(
    urls: list, timestamp, results: dict, lock, model, concurrency=3
):
    """
    URL을 비동기로 처리하며 동시 실행 제한을 둡니다.

    Args:
        urls: 처리할 URL 목록.
        timestamp: 타임스탬프.
        results: 결과 저장 딕셔너리.
        lock: asyncio.Lock() 객체.
        model: 필요시 전달할 모델 객체.
        concurrency: 동시에 실행할 작업 수.
    """
    semaphore = asyncio.Semaphore(concurrency)  # 동시 실행 제한

    async def sem_task(url):
        async with semaphore:  # 제한된 작업 수 안에서 실행
            scrapping_result = await process_url(url, results, model=model)
            results.update(scrapping_result)

    tasks = [sem_task(url) for url in urls]

    # 작업 진행 상황을 Rich Progress Bar로 표시
    with Progress(
        SpinnerColumn(),  # 로딩 스피너
        BarColumn(),  # 진행률 바
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),  # 퍼센트 표시
        TextColumn("현재 {task.completed}/{task.total} URLs 완료"),  # 완료된 개수
    ) as progress:
        task = progress.add_task("URL 처리 중...", total=len(urls))  # 작업 등록

        for coro in asyncio.as_completed(tasks):
            await coro
            progress.update(task, advance=1)  # 작업 상태 업데이트

    print("모든 작업이 완료되었습니다!")
    print(f"현재까지 총 {len(results)}개 url 작업완료")
