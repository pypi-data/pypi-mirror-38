from typhoon.base_manager import BaseManager
from typhoon.queues.dumper import NSQDumper
from .priority_queue_collection import PriorityQueueCollection
from .simple import SimpleQueue
from traceback import format_exception
from bson import json_util
import aiohttp
import requests
import json
import sys

class QueuesManager(BaseManager):

    def __init__(self, config, callback):

        super().__init__(callback, config, "queues")
        if not self.config["queues"]: return
        self.current_producer = None
        self.status = False
        self.config.finish_size = 10

        self.config.nsqlookupd_ip = "nsqlookupd:4161"
        self.queues = {}
        self.config.producers = []
        self.config.nsqd_addresses = []
        self.config["topics"] = self.get_topics()
        self.get_nsqd_ips()
        self.loop.create_task(self.init_queues())


    def get_nsqd_ips(self):
        address = []
        data = requests.get("http://nsqlookupd:4161/nodes").content
        nodes = json.loads(data.decode(), object_hook=json_util.object_hook)
        ips = []
        for producer in nodes.get("producers"):
            ip = producer["remote_address"].split(':')[0]
            ips.append(ip)
            address.append("{}:{}".format(ip, 4151))

        self.config.nsqd_addresses = list(set(ips))
        return address

    async def init_producers(self):
        self.config.dumper = NSQDumper(self.config)
        await self.config.dumper.init()


    def get_topics(self):
        try:
            data = requests.get("http://nsqlookupd:4161/topics").content
            return json.loads(data, object_hook=json_util.object_hook)["topics"]
        except:
            return []

    async def init_queues(self):
        await self.init_producers()
        if not self.config["queues"]: return
        for q in self.config["queues"]:
            if q.endswith("priority"):
                self.queues[q] = PriorityQueueCollection(self.config, q)
                if self.queues[q].config_queue.get("readable"):
                    self.queues[q].set_callback(self.on_message)
                    self.queues[q].start()
                continue
            self.queues[q] = SimpleQueue(self.config, name=q)
            if self.queues[q].config_queue.get("readable"):
                self.queues[q].set_callback(self.on_message)
                self.queues[q].init_reader()


    async def get_stats_nsqd(self, nsqdaddr):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://{}/stats?format=json".format(nsqdaddr), params={
                "format": "json"
            }) as response:
                data = await response.read()
                return json.loads(data.decode(), object_hook=json_util.object_hook)



    def get_topic_queues(self):
        queues = []
        for q in self.queues:
            if q.endswith("priority"):
                for p in self.queues[q].priorities:
                    queue = self.queues[q].priorities[p]
                    queues.append(queue.topic)
                continue
            queues.append(self.queues[q].topic)

        return queues

    async def pause(self, nsqdaddr, topic):

        async with aiohttp.ClientSession() as session:
            async with session.post("http://{}/channel/pause".format(nsqdaddr), params={
                "topic": topic,
                "channel": "tasks"
            }) as response:
                return response, await response.read()


    async def unpause(self, nsqdaddr, topic):
        async with aiohttp.ClientSession() as session:
            async with session.post("http://{}/channel/unpause".format(nsqdaddr), params={
                "topic": topic,
                "channel": "tasks"
            }) as response:
                return response, await response.read()

    async def empty_channel(self, nsqdaddr, topic):
        async with aiohttp.ClientSession() as session:
            async with session.post("http://{}/channel/empty".format(nsqdaddr), params={
                "topic": topic,
                "channel": "tasks"
            }) as response:
                return response, await response.read()

    async def empty_topic(self, nsqdaddr, topic):
        async with aiohttp.ClientSession() as session:
            async with session.post("http://{}/topic/empty".format(nsqdaddr), params={
                "topic": topic
            }) as response:
                return response, await response.read()

    def on_message(self, qname, task):
        self.loop.create_task(self.callback(qname, task))

    async def push(self, qname, task):
        task.finish()
        if qname.endswith("priority"):
            await self.queues[qname].priorities[task.task["priority"]].push(task.serialize())

        elif qname == "deferred":
            await self.queues[qname].delay_push(task.serialize(), task.task["processor"]["delay"])
        else:
            await self.queues[qname].push(task.serialize())


    def start(self):
        self.status = True
        try:
            for q in self.queues:
                if self.queues[q].config_queue.get("readable"):
                    pass
                    # self.loop.create_task(self.unpause())
                    # self.queues[q].start()
            print("Start Manager Queues")
        except:
            exc_info = sys.exc_info()
            exception_traceback = "".join(format_exception(*exc_info))
            print(exception_traceback)

    def stop(self):
        self.status = False
        try:
            for q in self.queues:
                if self.queues[q].config_queue.get("readable"):
                    self.queues[q].pause()

            print("Stop Manager Queues")
        except:
            exc_info = sys.exc_info()
            exception_traceback = "".join(format_exception(*exc_info))
            print(exception_traceback)