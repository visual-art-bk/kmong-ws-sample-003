import asyncio
from playwright.async_api import async_playwright
import os
from modules.utils.wrap_browser_page import WsBrowser
from modules.utils.Logger import Logger

# async def save_result(lock, results, url, status_k, status_v):
#     async with lock:
#         results[url][status_k] = status_v


async def fetch_page_source(url, folder_path=""):
    logger = Logger(
        log_file="logs/ws/fetch-page/exc.log", name="fetch_page_source"
    ).get_logger()

    status_key_result = "결과"
    timeout_page_goto = 10000
    sleep_before_page_loading = 2
    timeout_page_content_loading = 10000
    is_page_loaded = False

    async with async_playwright() as playwright:
        async with WsBrowser(playwright=playwright) as ws_browser:
            source = ""
            attempt_max = 4

            for attempt in range(attempt_max):
                if attempt == 0:
                    logger.info(f"fetch page 접속시도 / 타겟: {url}\n")
                else:
                    logger.exception(
                        f"fetch page 실패 / 타겟: {url}\n" f"{attempt}번 접속 재시도\n"
                    )

                is_goto_ok = await ws_browser.goto(url=url, timeout=timeout_page_goto)

                if is_goto_ok == False:
                    if attempt == attempt_max:
                        logger.exception(
                            f"{attempt}번 접속 재시도 초과\n",
                            f"fetch page 현재접속불가 / 타겟: {url}",
                        )
                    continue

                await asyncio.sleep(sleep_before_page_loading)

                source = await asyncio.wait_for(
                    ws_browser.page.content(), timeout=timeout_page_content_loading
                )

                if not "<img" in source:
                    source = ""

                is_page_loaded = True

                break

    return source
