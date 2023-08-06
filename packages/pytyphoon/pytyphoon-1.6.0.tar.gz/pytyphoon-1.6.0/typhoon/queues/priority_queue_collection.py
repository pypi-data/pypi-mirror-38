from .priority import PriorityQueue
import asyncio

class PriorityQueueCollection:
    def __init__(self, config, queue_name):
        self.loop = asyncio.get_event_loop()
        self.status = False
        self.queue_name = queue_name
        self.config = config
        self.config_queue = self.config.queues[self.queue_name]
        self.queue_args = (self.config, self.queue_name)
        self.priorities = {
            1: PriorityQueue(*self.queue_args, postfix="1"),
            2: PriorityQueue(*self.queue_args, postfix="2"),
            3: PriorityQueue(*self.queue_args, postfix="3")
        }
        self.current_queue = None
        if self.config_queue.get("readable"):
            self.init()

    def set_callback(self, callback):
        self.callback = callback

    def get_topics(self):
        return [self.priorities[p].topic for p in self.priorities]

    @property
    def concurrent(self):
        return self.config_queue["concurrent"]

    @concurrent.setter
    def concurrent(self, value):
        self.config_queue["concurrent"] = value
        for p in self.priorities:
            q = self.priorities[p]
            setattr(q, 'concurrent', value)

    @property
    def msg_timeout(self):
        return self.config_queue["msg_timeout"]

    @msg_timeout.setter
    def msg_timeout(self, value):
        self.config_queue["msg_timeout"] = value
        for p in self.priorities:
            q = self.priorities[p]
            q.msg_timeout = value

    def pause(self):
        for p in self.priorities:
            q = self.priorities[p]
            q.pause()
        self.status = False

    def start(self):
        self.status = True
        for p in self.priorities:
            q = self.priorities[p]
            q.status = True
            if not q.installed_reader:
                q.init_reader()

    def is_busy(self):
        return any([self.priorities[it].is_busy() for it in self.priorities])

    def is_depth(self, stats):
        status = False

        for stat in stats:
            if stat["depth"] > 0:
                status = True
                break

        return status

    def init(self):
        for p in self.priorities:
            queue = self.priorities[p]
            queue.set_callback(self.output)
            queue.msg_timeout = self.msg_timeout


    def output(self, message):
        self.callback(self.queue_name, message)
        # if self.is_busy() and self.config["pause_time"]:
        #     self.loop.create_task(self.run_pause_time())
