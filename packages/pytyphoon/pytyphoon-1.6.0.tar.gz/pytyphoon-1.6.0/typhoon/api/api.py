import random
import sys
import time
import json
import socket
import asyncio
import aiohttp

from aiohttp import web
from .base import BaseApi
from bson import json_util

class Api(BaseApi):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.app = web.Application(client_max_size=1024**3)
        self.port = None

    def init_router(self):
        pass

    async def request_register(self, session, params):
        register_service = self.state["register_service"]
        data = {
            "component":"registration",
            "event":"register",
            "additional":{
                "component": self.state["component_name"],
                "port": self.port,
                "project": self.state["project_name"]
            }
        }
        data["additional"].update(params)
        async with session.post("http://{}:{}".format(register_service["host"], register_service["port"]), json=data) as response:
            return response, await response.read()

    async def register_component(self, params={}):

        async with aiohttp.ClientSession() as session:
            response, content = await self.request_register(session, params)

    def up(self):
        try:
            self.init_router()
            self.port = self.get_port()
            if self.state["register_service"]:
                self.loop.create_task(self.register_component())
            web.run_app(self.app, port=self.port)
        except:
            self.up()
    def get_port(self):

        port = None

        for p in range(self.state["port"], 65535):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("", int(p)))
                s.listen(1)
                port = s.getsockname()[1]
                s.close()
                break
            except Exception as e:
                time.sleep(random.randint(0.0, 1.0))
                continue
        return port

    def close(self):
        self.app.shutdown()

    async def api_handler(self, request):
        body = {}
        try:
            body = await request.json()
        except:
            pass
        try:
            component = self.get_component({}, request)
            controller = self.components[component](request, self.state, self.get_subcomponents(request, body))
            headers, cookies, response = await controller.on_request()
        except Exception as e:
            return self.sendError(e)

        return web.Response(text=response.decode(), headers=headers)

    async def donor_handler(self, request):
        body = {}
        try:
            body = await request.json()
        except:
            pass
        try:
            await self.isValidRequest(request)
            component = self.get_component({}, request)
            controller = self.components[component](request, self.state, self.get_subcomponents(request, body))
            response = await controller.init()
        except Exception as e:
            return self.sendError(e)
        return web.Response(text=json.dumps(response), headers={
            "Content-Type": "application/json"
        })


    async def handler(self, request):

        response = None

        try:
            await self.isValidRequest(request)
            body = await request.json()
            component = self.get_component(body,request)
            controller = self.components[component](request, self.state, self.get_subcomponents(request, body))
            response = await controller.init()

        except Exception as e:

            return self.sendError(e)

        return web.Response(text=json.dumps(response, default=json_util.default), headers={
            "Content-Type": "application/json"
        })