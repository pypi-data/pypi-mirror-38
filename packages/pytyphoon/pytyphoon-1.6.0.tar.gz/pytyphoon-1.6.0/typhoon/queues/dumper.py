import functools
import asyncio
import nsq

class NSQDumper:
    def __init__(self, config):
        self.loop = asyncio.get_event_loop()
        self.config = config
        self.concurrent = self.config.concurrent_push_to_queue or 500
        self.semaphore = asyncio.Semaphore(value=self.concurrent)
        self.tasks = []
        self.producer = nsq.Writer(self.tcp_addresses)
        self.is_ready = True


    @property
    def tcp_addresses(self):
        return ["{}:4150".format(ip) for ip in self.config.nsqd_addresses]

    def restart_writer(self):
        self.producer = nsq.Writer(self.tcp_addresses)

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
            count+=1
            await asyncio.sleep(0.5)


    async def retry(self, topic, message):
        await asyncio.sleep(1)
        await self.push_to_nsq(topic, message)


    def pubcb(self, message, topic, conn, data):
        if isinstance(data, nsq.protocol.Error) and 'no open connections' in str(data):
            self.is_ready = False
            self.restart_writer()
            self.loop.create_task(self.retry(topic, message))
        else:
            self.is_ready = True

    async def push_to_nsq(self, topic, message, delay=0):

        pubcb = functools.partial(self.pubcb, message, topic)

        if not delay:
            self.producer.pub(topic, message.encode(), callback=pubcb)
        else:
            self.producer.dpub(topic, delay*1000, message.encode(), callback=pubcb)
        await asyncio.sleep(0.5)

    async def add_task(self, topic, task, delay):
        self.tasks.append(asyncio.ensure_future(self.push_to_nsq(topic, task, delay)))
        await self.semaphore.acquire()


    async def push(self, topic, task, delay):
        while True:
            if self.is_ready:
                await self.add_task(topic, task, delay)
                break
            await asyncio.sleep(1)

if __name__ == "__main__":

    async def test(loop):
        await asyncio.wait([])

    loop = asyncio.get_event_loop()
    loop.create_task(test(loop))
    loop.run_forever()



