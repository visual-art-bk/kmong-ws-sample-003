import time
from .Logger import Logger
import asyncio

class Timer:
    def __init__(self, log_file="logs/time/timer.log") -> None:
        self._start_time = None
        self._end_time = None
        self._log_file = log_file
        self._logger = Logger(log_file=self._log_file, name="timer").get_logger()
        pass

    async def start(self):
        self.start_time = asyncio.get_event_loop().time()

    async def measure(self, desc=""):
        # self._check_timer_running()

        self._end_time = time.time()

        elapsed_time = asyncio.get_event_loop().time() - self.start_time

        self._logger.info(f"총 실행 시간: {elapsed_time:.2f}ms / desc: {desc}")

    def _check_timer_running(self):
        try:
            if self._start_time == None:
                raise Exception
        except Exception as e:
            self._logger.exception(f"타임측정 시간초기화가 되지 않았음 / timer.start 호출 필요")
