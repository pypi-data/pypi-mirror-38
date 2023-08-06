import asyncio
from typhoon.queues.queues_manager import QueuesManager


class BaseComponent:

    def __init__(self, config):
        self.loop = asyncio.get_event_loop()

        self.config = config
        self.queues_manager = QueuesManager(self.config, self.on_message)
        self.loop.create_task(self.on_start())
        self.finished_task = False
        self.message_at = None

    def on_message(self, queue_name, message):
        raise NotImplementedError

    async def waiting_finish(self):
        last_message = self.message_at
        while True:
            await asyncio.sleep(60*5)
            if last_message == self.message_at:
                print("finish ", self.config["component_name"])
                await self.on_finish()
                break

            last_message = self.message_at

        self.finished_task.done()
        self.finished_task = False

    async def on_start(self):
        raise NotImplementedError

    async def on_finish(self):
        pass


    def run(self):
        self.queues_manager.start()

    def stop(self):
        self.queues_manager.stop()
        for task in asyncio.Task.all_tasks():
            try:
                pass
                # task.cancel() #
            except:
                pass
