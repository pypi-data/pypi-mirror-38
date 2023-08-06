import asyncio
from typing import Dict, Callable

from actorio import MessageQueue, Message
from actorio.errors import ActorioException
from actorio.mlp_async import ReusableTask


class Actor:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._mainloop_task: asyncio.Task = None
        self._input_tasks: Dict[ReusableTask, Callable] = dict()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return asyncio.get_event_loop()

    async def _mainloop(self):
        while True:

            try:
                finished_tasks, _ = await asyncio.wait([rt.task for rt in self._input_tasks], return_when=asyncio.FIRST_COMPLETED)
            except asyncio.CancelledError:
                break

            for finished_task in finished_tasks:
                reusable_task, coro_to_run = next((rt, coro) for rt, coro in self._input_tasks.items() if rt.task == finished_task)
                task = self.loop.create_task(coro_to_run(finished_task))
                try:
                    await asyncio.shield(task)
                    reusable_task.arm()
                except asyncio.CancelledError:
                    await task
                    return

    def register_task_handler(self, input_task: Callable, coro_to_run: Callable):
        self._input_tasks[ReusableTask(input_task)] = coro_to_run

    def __await__(self):
        return self._mainloop_task.__await__()

    async def start(self):
        self._mainloop_task = self.loop.create_task(self._mainloop())

    async def __aenter__(self):
        await self.start()
        return self

    async def stop(self):
        self._mainloop_task.cancel()
        for rt in self._input_tasks:
            rt.task.cancel()

        await asyncio.wait([rt.task for rt in self._input_tasks] + [self], return_when=asyncio.ALL_COMPLETED)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()


class UnhandledMessage(ActorioException, NotImplementedError):

    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(*args)


class MessageInputActor(Actor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.inbox = MessageQueue()

    async def _handle_message(self, task: asyncio.Task):
        message: Message = task.result()
        return await self.handle_message(message)

    async def handle_message(self, message: Message):
        raise UnhandledMessage(message)

    async def start(self):
        self.register_task_handler(self.inbox.get, self._handle_message)
        return await super().start()
