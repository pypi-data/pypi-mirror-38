import nsq
import json
import asyncio
import requests
import aiohttp
# from asyncnsq import create_nsq_consumer
from bson import json_util

class BaseQueue:
    def __init__(self, config, name, postfix):
        self.name = name
        self.status = False
        self.installed_reader = False
        self.config = config
        self.addresses = self.config.nsqd_addresses
        self.loop = asyncio.get_event_loop()
        self.config_queue = self.config.queues[self.name]
        self.channel = self.config_queue["channel"]
        self.postfix = postfix
        self.topic = self.get_topic()
        self.test_count_start = 1



    def get_topic(self):
        topic = "{}_{}".format(self.config["project_name"], self.config_queue["topic"] + self.postfix)

        if not self.config_queue.get("share"):
            topic = "{}_{}".format(self.config["component_name"],topic)

        if self.config["debug"]:
            topic = "{}_debug".format(topic)

        return topic


    def install_topic(self):
        if self.topic in self.config["topics"]: return
        http_addresses = ["{}:4151".format(ip) for ip in self.addresses]
        for nsqd_ip in http_addresses:
            requests.post("http://{}/topic/create?topic={}".format(nsqd_ip, self.topic))
            requests.post("http://{}/channel/create?topic={}&channel=tasks".format(nsqd_ip, self.topic))

        self.config["topics"].append(self.topic)


    def init_reader(self):
        if self.installed_reader: return
        self.install_topic()
        print (self.concurrent, self.topic, self.channel, ".......................!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.reader = nsq.Reader(
            topic=self.topic, channel=self.channel, message_handler=self.message_handler,
            lookupd_connect_timeout=10, requeue_delay=10, msg_timeout=self.msg_timeout,
            lookupd_http_addresses=[self.config.nsqlookupd_ip], max_in_flight=self.concurrent, snappy=True
        )
        self.installed_reader = True
        # if not self.status:
        #     self.reader.set_max_in_flight(0)


    async def reading(self):
        for waiter in self.reader.wait_messages():
            message = await waiter
            print(message.body)
            await message.fin()

    async def init_reader_(self):
        if self.installed_reader: return
        self.install_topic()

        self.reader = await create_nsq_consumer(
            lookupd_http_addresses=[
                ('nsqlookupd', 4161)],
            max_in_flight=self.concurrent)

        await self.reader.subscribe(self.topic, self.channel)

        self.loop.create_task(self.reading())

    @property
    def msg_timeout(self):
        return self.config_queue["msg_timeout"]

    @msg_timeout.setter
    def msg_timeout(self, value):
        self.config_queue["msg_timeout"] = value

    def is_busy(self):
        return self.reader.is_starved()

    def pause(self):
        self.status = False
        # self.reader.set_max_in_flight(0)

    def set_callback(self, callback):
        self.callback = callback

    @property
    def concurrent(self):
        return self.config_queue["concurrent"]

    @concurrent.setter
    def concurrent(self, value):
        self.config_queue["concurrent"] = value
        if self.status:
            print("change concurrent on " + self.topic, self.concurrent)
            # self.reader.set_max_in_flight(0)
            # self.init_reader()
            # self.reader.set_max_in_flight(self.concurrent)

    def start(self):
        print(self.test_count_start, "WHAT IS IT ? ")
        if not self.status:
            self.status = True
            print("Start Queue", self.topic, self.concurrent)

            # self.reader.set_max_in_flight(self.concurrent)
        self.test_count_start = +1



    def get_stats(self):
        stats = []
        for ip in self.addresses:
            data = json.loads(requests.get('http://{}:4151/stats?format=json&topic={}'.format(ip,self.topic)).content.decode(), object_hook=json_util.object_hook)
            for topic in data["topics"]:
                if topic["topic_name"] != self.topic:
                    continue

                for channel in topic["channels"]:
                    if channel["channel_name"] != self.channel:
                        continue
                    stats.append(channel)
        return stats

    async def queue_checker(self, message):
        raise NotImplementedError

    def message_handler(self, message):
        raise NotImplementedError

    async def delay_push(self, message, delay):
        await self.config.dumper.push(self.topic, message, delay)
        # self.config.writer.dpub(self.topic, delay * 1000, message.encode())

        # await asyncio.sleep(1)

        # current_producer = self.config.nsqd_addresses[self.config.current_producer.get()]
        #
        # async with aiohttp.ClientSession() as session:
        #     async with session.post("http://{}:{}/pub?topic={}&delay={}".format(current_producer, 4151, self.topic, delay*1000), data=message.encode()) as response:
        #         data = await response.read()
                # print(data)
                # return json.loads(data.decode())

    async def push(self, message):
        await self.config.dumper.push(self.topic, message, 0)

        # self.config.writer.pub(self.topic, message.encode())

        # await asyncio.sleep(1)

        # current_producer = self.config.nsqd_addresses[self.config.current_producer.get()]
        #
        # async with aiohttp.ClientSession() as session:
        #     async with session.post("http://{}:{}/pub?topic={}".format(current_producer, 4151, self.topic), data=message.encode()) as response:
        #         data = await response.read()
                # print(data)
                # return json.loads(data.decode())


        # await current_producer.pub(self.topic, message.encode())