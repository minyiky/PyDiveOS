try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Protocol, List, Tuple

import time

import uasyncio

if TYPE_CHECKING:

    class Subscriber(Protocol):
        def update_time(self, time: Tuple[int, int, int, int, int, int, int, int, int]):
            pass


class Clock:
    _instance = None

    # Implement MenuBar as a singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Clock, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.time = time.localtime()
        self._subscribers: List[Subscriber] = []
        uasyncio.create_task(self.update_time())

    def add_subscriber(self, subscriber: Subscriber):
        self._subscribers.append(subscriber)

    async def update_time(self):
        ticks = time.ticks_ms()
        while 1:
            if time.ticks_diff(time.ticks_ms(), ticks) > 1000:
                ticks = time.ticks_ms()
                localtime = time.localtime()
                for sub in self._subscribers:
                    sub.update_time(localtime)
            await uasyncio.sleep(0.05)
