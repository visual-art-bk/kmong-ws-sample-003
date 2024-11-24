import asyncio
from playwright.async_api import async_playwright
import os


# async def save_result(lock, results, url, status_k, status_v):
#     async with lock:
#         results[url][status_k] = status_v


async def fetch_page_source(url, folder_path=""):
    status_key_result = "결과"
    timeout_page_goto = 40
    sleep_before_page_loading = 2
    timeout_page_content_loading = 40
    is_page_loaded = False

    # dist 디렉토리 내의 Playwright 브라우저 경로 설정
    driavers_path = os.path.join(
        os.getcwd(), "drivers"
    ) 
    
    browser_path = os.path.join(
        driavers_path,
        "ms-playwright",
        "chromium-1140",
        "chrome-win",
        "chrome.exe",
    )

    if not os.path.exists(browser_path):
        print(f"[ERROR] 브라우저 실행 파일을 찾을 수 없습니다: {browser_path}")
        return None

    async with async_playwright() as playwright:
        # Playwright 브라우저 경로 지정
        browser = await playwright.chromium.launch(
            headless=False, executable_path=browser_path
        )

        context = await browser.new_context()
        page = await context.new_page()
        source = ""

        for attempt in range(5):
            try:
                await asyncio.wait_for(page.goto(url), timeout=timeout_page_goto)
                await asyncio.sleep(sleep_before_page_loading)
                source = await asyncio.wait_for(
                    page.content(), timeout=timeout_page_content_loading
                )

                if not "<img" in source:
                    source = ""
                    # await save_result(
                    #     lock,
                    #     results,
                    #     url,
                    #     status_k=status_key_result,
                    #     status_v="페이지로딩성공-사진없음",
                    # )

                is_page_loaded = True
                break

            except asyncio.TimeoutError:
                pass
                # await save_result(
                #     lock,
                #     results,
                #     url,
                #     status_k=status_key_result,
                #     status_v="페이지로딩실패-시간초과",
                # )

            except Exception:
                pass
                # await save_result(
                #     lock,
                #     results,
                #     url,
                #     status_k=status_key_result,
                #     status_v="패이지로딩실패-알수없는오류",
                # )

            finally:
                await browser.close()

    return source
