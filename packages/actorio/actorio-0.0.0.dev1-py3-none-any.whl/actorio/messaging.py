import asyncio


class Message:
    def __init__(self, *args, reply_to: "MessageQueue" = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reply_to = reply_to


class MessageQueue:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = asyncio.Queue()

    async def put(self, item: Message):
        return await self._queue.put(item)

    def put_nowait(self, item: Message):
        return self._queue.put_nowait(item)

    async def get(self) -> Message:
        return await self._queue.get()

    def get_nowait(self) -> Message:
        return self._queue.get_nowait()
