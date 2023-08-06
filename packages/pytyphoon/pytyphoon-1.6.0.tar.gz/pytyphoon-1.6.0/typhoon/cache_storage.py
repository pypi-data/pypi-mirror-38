import pymongo
import aioredis
import motor.motor_asyncio

class CacheStorage:

    def __init__(self, config, loop):
        self.config = config
        self.loop = loop
        self.services = {
            "mongo": self.init_mongo,
            "redis": self.init_redis
        }

    async def init_connection(self):
        self.mode = "debug" if self.config["debug"] else "production"
        for service in self.config["services"]:
            for config_set in self.config["services"][service][self.mode]:
                await self.services[service](config_set)

    def get_db_settings(self, config_set):
        return config_set["name"], config_set["details"], config_set.get("db_names")

    async def init_redis(self, config_set):
        name, details, *_ = self.get_db_settings(config_set)
        self.redis_con = await aioredis.create_redis(address=(details["host"], details["port"]), password=details["password"])

    async def create_index_collection(self, collection, field, sort_type="DESC"):
        field = (field, pymongo.DESCENDING if sort_type == "DESC" else pymongo.ASCENDING)
        await collection.create_index([field], background=True)

    async def create_compound_index(self, collection, fields):
        await collection.create_index([(field, pymongo.DESCENDING) for field in fields], background=True)

    async def init_mongo(self, config_set):
        name, details, db_names = self.get_db_settings(config_set)

        setattr(self, name, motor.motor_asyncio.AsyncIOMotorClient(
            **details
        ))

        for db_name in db_names:
            setattr(self, "{0}_{1}".format(name, db_name), getattr(self, name)[db_name])

    def get_mongo_collection(self, collection_name, db_name=None, client_name=None):
        _db_name = self.config["project_name"] if db_name is None else db_name
        _client_name = self.config["services"]["mongo"][self.mode][0]["name"] if client_name is None else client_name
        return getattr(self, "{0}_{1}".format(_client_name, _db_name))[collection_name]

    async def set(self, key, value):
        await self.redis_con.set(key, value)

    async def scan(self, cur, match):
        return await self.redis_con.scan(cur, match=match, count=100)

    async def delete(self, keys):
        await self.redis_con.delete(*keys)

    async def set_ex(self, key, value, time_in_sec):
        await self.redis_con.setex(key, time_in_sec, value)

    async def incrby(self, key, value):
        await self.redis_con.incrby(key, value)


    async def mget(self, keys):
        return await self.redis_con.mget(*keys)

    async def mset(self, *pairs):
        """pairs key, value"""
        await self.redis_con.mset(*pairs)

    async def get(self, key):
        return await self.redis_con.get(key)

    async def increment(self, key, amount=1):
        await self.redis_con.incrby(key, amount)




async def test(loop, config):
    storage = CacheStorage(config, loop)
    await storage.init_connection()
    cur = b'0'
    counts = 0
    while cur:
        cur, keys = await storage.scan(cur, '{}:*'.format("stream"))
        if keys:
            await storage.delete(keys)
            counts += len(keys)

    print(counts)

# IT'S ONLY FOR METHODS TESTING
if __name__ == "__main__":
    import asyncio
    from typhoon.state.base import BaseStateManager

    config = {
        "project_name": "test",
        "component_name": "fetcher",
        "timeout": 1,
        "debug": True,
        "services": {
            "redis": {
                "production": [
                    {
                        "name": "main",
                        "details":{
                            "host": "localhost",
                            "port": 6380,
                            "password": None
                        }
                    }
                ],
                "debug": [
                    {
                        "name": "main",
                        "details":{
                            "host": "localhost",
                            "port": 6380,
                            "password": None
                        }
                    }
                ]
            }
        }
    }
    config = BaseStateManager(config)
    loop = asyncio.get_event_loop()

    loop.create_task(test(loop, config))
    loop.run_forever()
    # loop.run_forever()
    # loop.run_until_complete(main())
