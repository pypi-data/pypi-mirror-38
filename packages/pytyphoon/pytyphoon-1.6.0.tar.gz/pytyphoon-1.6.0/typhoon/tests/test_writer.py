import nsq

import time
# producer = nsq.Writer(nsqd_tcp_addresses=['78.46.81.238:4150'])
# print(producer)
# time.sleep(4)
# def pubcb(conn, data):
#     print(conn, data)
#
# for i in range(10000):
#     message = "test{}".format(i)
#     producer.pub("test", message.encode(), callback=pubcb)


import nsq
import tornado.ioloop
import datetime
import random
import json
import asyncio



class NSQDumper:
    def __init__(self, producer, cuncurrent):
        self.loop = asyncio.get_event_loop()
        self.concurrent = cuncurrent or 100
        self.semaphore = asyncio.Semaphore(value=self.concurrent)
        self.tasks = []
        self.producer = producer
        self.is_ready = True

    async def init(self):
        await asyncio.sleep(2)
        self.loop.create_task(self.process())

    async def done_tasks(self):
        if not self.tasks: return
        await asyncio.wait(self.tasks)
        [self.semaphore.release() for flush in range(self.concurrent)]
        self.tasks.clear()

    async def process(self):
        count = 0
        while True:
            if self.semaphore.locked():
                self.is_ready = False
                await self.done_tasks()
                # print("done batch", self.concurrent)
                self.is_ready = True
                continue
            count += 1
            await asyncio.sleep(0.5)

    async def push_to_nsq(self, topic, message, delay=0):
        if not delay:
            self.producer.pub(topic, message.encode())
        else:
            self.producer.dpub(topic, delay * 1000, message.encode())
        await asyncio.sleep(1)

    async def add_task(self, topic, task, delay):
        self.tasks.append(asyncio.ensure_future(self.push_to_nsq(topic, task, delay)))
        # self.tasks.append(self.push_to_nsq())
        await self.semaphore.acquire()

    async def push(self, topic, task, delay):
        while True:
            if self.is_ready:
                await self.add_task(topic, task, delay)
                break
            await asyncio.sleep(1)


import time

if __name__ == "__main__":
    count = 0
    start = time.time()


    async def checker():
        while True:
            await asyncio.sleep(5)
            end = time.time()
            print(count, (end - start) / 60)


    def pubcb(conn, data):
        if isinstance(data, nsq.protocol.Error) and 'no open connections' in str(data):
            print(data)

    async def main(loop):
        global count
        producer = nsq.Writer(nsqd_tcp_addresses=['78.46.81.238:4150'])
        dumper = NSQDumper(producer, 2000)
        await dumper.init()
        loop.create_task(checker())


        for i in range(10000000):
            message = "test{}".format(i) * 1024
            await dumper.push("test", message, 0)
            count+=1

        # print(await collection.count({"marketplace" : "target.com", "images":{"$exists":True}}))

        # return
        # dumper = NSQDumper(producer, 1000)
        # await dumper.init()
        # print (collection.count({"marketplace" : "target.com", "images":{"$exists":True}}))
        # global count


        # await producer.pub("images_priority_f3_debug", task.encode())
        # await dumper.push("images_priority_f3_debug", task, 0)
        # print(task)

            # break
        pass


    from tornado.platform.asyncio import AsyncIOMainLoop

    loop = asyncio.get_event_loop()
    AsyncIOMainLoop().install()
    loop.create_task(main(loop))
    loop.run_forever()