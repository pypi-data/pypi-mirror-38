import asyncio
import json
import time
from typhoon.tasks.base import BaseTask
from bson import json_util


class TestAsync(BaseTask):
    def __init__(self, config, message=None, queue_name=None, task=None):
        super().__init__(config, json.loads(message, object_hook=json_util.object_hook), queue_name)

        self._init_attributes()
        self.set_component_task()

    def _init_attributes(self):
        self.loop = asyncio.get_event_loop()

    def done(self):

        finished_at = time.time()
        self.component_task["save"]["system"].update([
            ("added_at", self.added_at),
            ("finished_at", finished_at),
            ("duration", finished_at - self.added_at)
        ])