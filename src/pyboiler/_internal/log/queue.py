import queue as que
import threading


class _Queue:
    __slots__ = ("queue", "thread")

    def __init__(self):
        self.queue = que.Queue()
        self.thread = threading.Thread(target=self._main, daemon=True)
        self.thread.start()

    def _main(self):
        while True:
            handlers = self.queue.get()
            if handlers is None:
                break
            for handler in handlers:
                handler()

    def stop(self):
        self.queue.put_nowait(None)
        self.queue.join()


class Queue:
    __instance = None
    __slots__ = "_queue"

    def __new__(cls):
        if cls.__instance is None:
            inst = object.__new__(cls)
            inst._queue = _Queue()
            cls.__instance = inst
        return cls.__instance

    def stop(self):
        self._queue.stop()

    def add(self, handlers: list):
        self._queue.queue.put_nowait(handlers)
