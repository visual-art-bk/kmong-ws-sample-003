import asyncio

import nodriver as uc


async def fetch_page_source(lock, url, folder_path, results=[]):
    browser = await uc.start()

    try:
        page = await asyncio.wait_for(
            browser.get(url), timeout=10
        )  # 10초의 타임아웃 설정

        count = 0
        while True:
            if count > 5:
                async with lock:
                    results[url]["결과"] = "실패"
                return ""

            await asyncio.sleep(3)
            count += 1

            try:
                source = await asyncio.wait_for(page.get_content(), timeout=5)
            except asyncio.TimeoutError:
                async with lock:
                    results[url]["결과"] = "실패"
                return ""

            if "<img" in source:
                return source
    except asyncio.TimeoutError:
        async with lock:
            results[url]["결과"] = "실패"
        return ""
    except Exception:
        async with lock:
            results[url]["결과"] = "실패"
        return ""
    finally:
        browser.stop()
