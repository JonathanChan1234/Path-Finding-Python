import threading

from pygame import event as PyEvent, USEREVENT
from threading import Thread
import time
import asyncio


class AsyncAlgorithmThread(Thread):
    EVENT_ID = USEREVENT + 3

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print(f'In thread: {threading.current_thread().name}')
        print('worker process started')
        time.sleep(10)
        # PyEvent.post(PyEvent.Event(AsyncAlgorithmThread.EVENT_ID, {"value": [1, 2, 3, 4, 6]}))


async def test_async_task(id, callback):
    print(f'In thread: {threading.current_thread().name}')
    print(f'test_async_task id {id} is started')
    await asyncio.sleep(3)
    callback(id)
    print(f'test_async_task id {id} finished')


def callback(id):
    print(f'callback function from task {id}')


async def main():
    tasks = []
    task = asyncio.create_task(test_async_task(id, callback))
    await task


if __name__ == '__main__':
    while True:
        print('looping')
        # test_thread = AsyncAlgorithmThread()
        # test_thread.start()
        asyncio.run(main())
