import asyncio
import json
import time
from typhoon.tasks.base import BaseTask
from bson import json_util


class BaseAsync(BaseTask):
    def __init__(self, config, message=None, queue_name=None, task=None):
        super().__init__(config, task, queue_name)
        self.message = message
        self._init_attributes()
        self.set_component_task()
        self.is_done = False
        self.type = "async"

    def _init_attributes(self):
        if self.message and self.queue_name:
            self.task = json.loads(self.message.body, object_hook=json_util.object_hook)
            self.config_queue = self.config.queues[self.queue_name]
            self.loop = asyncio.get_event_loop()
            self.touching_task = self.loop.create_task(self.touching())

    def finish(self):
        finished_at = time.time()
        self.component_task["save"]["system"].update([
            ("added_at", self.added_at),
            ("finished_at", finished_at),
            ("duration", finished_at - self.added_at)
        ])

    def done(self):
        self.is_done = True

        if self.message and self.queue_name:
            self.touching_task.cancel()
            self.message.finish()


    async def touching(self):
        while not self.is_done:
            self.message.touch()
            await asyncio.sleep(self.get_latency())

    def get_latency(self):
        return self.config_queue["msg_timeout"] // 2
