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
from modules.scrappers import download_images, process_new_urls
import time

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
model.generate_content("Hi")
os.system("cls")

new_urls = set()
if __name__ == "__main__":
    print("Start v.1.0.4")

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    absl.logging.set_verbosity("error")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    urls = read_urls(path="url.txt")

    results = {}
    lock = asyncio.Lock()

    # 파일 변경 감지 핸들러
    class FileHandler(FileSystemEventHandler):
        def __init__(self, observed_file, callback):
            self.observed_file = observed_file
            self.callback = callback

        def on_modified(self, event):
            if event.src_path.endswith(self.observed_file):
                self.callback()

    # 파일 변경 감지로 새 URL 읽기
    def monitor_file():
        new_urls = read_urls("new_url.txt") - read_urls("url.txt")
        if new_urls:
            print(f"새로운 URL 발견: {new_urls}")
            asyncio.run(
                process_new_urls(
                    urls=new_urls,
                    lock=lock,
                    model=model,
                    results=results,
                    timestamp=timestamp,
                )
            )
            # 기존 URL 리스트 업데이트
            with open("url.txt", "a", encoding="utf-8") as f:
                for url in new_urls:
                    f.write(url + "\n")

    uc.loop().run_until_complete(
        process_new_urls(
            urls=urls, lock=lock, model=model, results=results, timestamp=timestamp
        )
    )

    final = list(results.values())

    make_excel(
        final_result=final,
        timestamp=timestamp,
    )

    # 파일 변경 감지 설정
    observer = Observer()
    event_handler = FileHandler("new_url.txt", monitor_file)
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    print("새 URL 감지 중... 종료하려면 Ctrl+C를 누르세요.")

    try:
        while True:
            time.sleep(1)
            user_input = input("신규 url 추가 대기중. (종료하려면 'exit' 입력): ")
            if user_input.lower() == "exit":
                print("프로그램을 종료합니다.")
                break
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # while True:
    #     user_input = input("명령을 입력하세요 (종료하려면 'exit' 입력): ")
    #     if user_input.lower() == "exit":
    #         print("프로그램을 종료합니다.")
    #         break
