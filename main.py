import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import io
import sys
import os, asyncio, urllib.parse, json
from datetime import datetime, timedelta
import google.generativeai as genai
from tqdm.asyncio import tqdm
import absl.logging
from modules.utils.file_utils import read_urls, make_excel
from modules.scrappers import download_images, process_new_urls
from modules.utils.Logger import Logger

# 설정된 종료 시간
END_DATE = datetime(2024, 11, 30, 23, 00)  # 예: 2024년 12월 1일 0시 0분

logger = Logger(name="main", log_file="logs/main.log").get_logger()

with open("config.json", "r", encoding="utf-8") as file:
    config_data = json.load(file)
    api_key = config_data["api_key"]
    model_name = config_data["model"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name=model_name,
    generation_config={
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 500,
        "response_mime_type": "application/json",
    },
)

new_urls = set()
inited_new_url = read_urls(path="new_url.txt")

processed_urls = set()
results = {}

absl.logging.set_verbosity("error")

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

urls = read_urls(path="url.txt")

lock = asyncio.Lock()

file_change_queue = asyncio.Queue()  # 파일 변경 이벤트를 저장하는 큐


async def scrap_urls(urls, results: dict):
    scraped_results = await process_new_urls(
        model=model, timestamp=timestamp, urls=urls
    )

    # 전역 results에 새로운 데이터를 추가
    results.update(scraped_results)


class FileHandler(FileSystemEventHandler):
    def __init__(self, observed_file, loop):
        self.observed_file = observed_file
        self.loop = loop

    def on_modified(self, event):
        if event.src_path.endswith(self.observed_file):
            print(f"DEBUG: {self.observed_file} 변경 감지됨")
            # 비동기로 큐에 이벤트 추가
            self.loop.call_soon_threadsafe(
                asyncio.create_task, file_change_queue.put(event)
            )


async def monitor_file():
    global results  # 전역 변수로 사용

    new_urls = read_urls("new_url.txt") - read_urls("url.txt")

    # 이미 처리된 URL 필터링
    new_urls -= processed_urls

    if new_urls:
        print(f"\n 파일변경모니터링중... 새로운 URL 발견: {new_urls}")

        await scrap_urls(urls=new_urls, results=results)

        # 처리된 URL 추가
        processed_urls.update(new_urls)

        with open("url.txt", "a", encoding="utf-8") as f:
            for url in new_urls:
                f.write("\n" + url + "\n")
    else:
        print(f"\n 파일변경모니터링중.. 새로운 URL 없음: {new_urls}")


async def main_loop():
    logger.info("로그 테스트 / main_loop")

    global results
    did_first_loop = False

    # 파일 변경 감지 설정
    observer = Observer()
    event_handler = FileHandler("new_url.txt", asyncio.get_event_loop())
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            # 종료 시간 확인
            now = datetime.now()
            if now >= END_DATE:
                print(
                    f"경고: 프로그램 사용 기한이 {END_DATE}에 도달했습니다. 실행을 중단합니다."
                )
                break

            print("DEBUG: main_loop 실행 시작")

            # 기존 URL 처리
            if did_first_loop == False:

                await scrap_urls(urls=urls, results=results)

                final = list(results.values())

                try:
                    await make_excel(
                        final_result=final,
                        timestamp=timestamp,
                    )
                except Exception as e:
                    print(f"엑셀저장오류발생: {e}")
                    traceback.print_exc()
                finally:
                    did_first_loop = True
                    print(f"엑셀저장완료")

            # 파일 변경 이벤트 처리
            print("DEBUG: 파일 변경 대기 중...")
            event = await file_change_queue.get()  # 큐에서 이벤트 가져오기
            print(f"DEBUG: 변경 이벤트 처리: {event.src_path}")

            # 파일 변경 감지 후 monitor_file 호출
            await monitor_file()

            # 큐가 비었는지 확인 후 엑셀 저장
            if file_change_queue.empty():  # 큐가 비었을 때만 실행
                print("DEBUG: 큐가 비었음. 엑셀 저장 실행.")
                final = list(results.values())

                await make_excel(
                    final_result=final,
                    timestamp=timestamp,
                )
            else:
                print("DEBUG: 큐가 비지 않음. 엑셀 저장 대기.")

    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()


if __name__ == "__main__":
    logger.info("Start v.1.0.5")

    asyncio.run(main_loop())
