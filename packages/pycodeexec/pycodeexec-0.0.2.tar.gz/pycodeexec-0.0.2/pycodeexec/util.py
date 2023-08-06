import time
from asyncio import sleep
from threading import Thread


class BlockTimer:
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"{self.label}: {round((time.time() - self.start)*1000, 2)}ms")


time_this = BlockTimer



