from jsonschema import validate
from typhoon.api.base import BaseApi
import inspect
from base64 import b64encode
import json
import aiohttp

class BaseComponent(BaseApi):

    def __init__(self, request, state, sub_components=None):
        super().__init__()
        self.sub_components = sub_components
        self.state = state
        self.component = None
        self.request = request
        self.method = self.request.method
        self.headers = self.request.headers
        self.cookies = self.request.cookies
        self.events = {}
        self.schemas = {}
        self.attributes = {}
        self.components = {}
        self.editable_attributes = []
        self.base_errors = {
            0: "Event not found",
            100: "Schema isn't valid",
            200: "Sub component isn't defined",
            300: "HTTP Method not allowed",
            400: "Class method for API event is not defined"
        }

        self.errors = {
            0: "Attribute not found",
            100: "Attribute isn't editable",
            200: "Value not found",
            300: "Value isn't valid"
        }

    def get_mongo_collection(self, *, collection_name, db_name=None, client_name="main"):
        return self.state.cache_storage.get_mongo_collection(collection_name, db_name, client_name)

    async def execute_sync_in_component(self, component, method):
        assert component == "fetcher" or component == "processor", "component name must be fetcher or processor"


        task = {
            "component": "proxy",
            "event": "to_component",
            "request": {
                "body": {
                    "component": "application",
                    "event": "execute_method",
                    "method": method
                },
                "routes": [component]
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://{self.state["project_name"]}:5000', json=task) as response:
                return await response.json()



    async def send_to_component(self, component, data, callback):
        assert component == "fetcher" or component == "processor", "component name must be fetcher or processor"
        assert isinstance(callback, str), "callback name is required"
        assert isinstance(data, dict), "data must be dict"

        new_task = {
            "fetcher": {
                "content": (b64encode((json.dumps(data)).encode())).decode()
            },
            "processor": {
                "callback": {
                    "name": callback,
                    "type": "pipelines_group"
                },
                "strategy": "text",
                "save": {
                    "project": {}
                }
            },
            "scheduler": {
                "age": 10
            },
            "priority": 3,
            "url": "http://pipeline.com",
        }
        topic = "{0}_priority_{1}{2}".format(self.state["project_name"], component[0], 3)
        if self.state["debug"]:
            topic = "{0}_debug".format(topic)


        return await self.state.dumper.push(topic, json.dumps(new_task), 0)



    def isValidSubComponent(self, sub_component):
        if not self.components.get(sub_component):
            raise Exception(self.base_errors[200])

    def is_body(self):
        return self.request.method in ["PUT", "POST"]

    def get_sub_component(self):
        sub_component = None

        if len(self.sub_components) > 0:
            sub_component = self.sub_components[0]
            self.sub_components = self.sub_components[1:]
            self.isValidSubComponent(sub_component)

        return sub_component

    async def isValidEvent(self):
        body = {}
        if self.is_body():
            body = await self.request.json()

        self.event = self.get_event(body, self.request)

        if not self.events.get(self.event):
            raise Exception(self.base_errors[0])

        if isinstance(self.events[self.event], dict) and not self.events[self.event]["type"].lower() == self.request.method.lower():
            raise Exception(self.base_errors[300])

        if isinstance(self.events[self.event], dict) and not getattr(self, self.event):
            raise Exception(self.base_errors[400])

        if self.schemas.get(self.event) and self.is_body():
            validate(body, self.schemas[self.event])



    async def execute_event(self):
        if inspect.isclass(self.events[self.event]):
            events_class = self.events[self.event](self.state, self.request)
            executor = getattr(events_class, self.event)
        elif isinstance(self.events[self.event], dict):
            executor = self.events[self.event]["method"]
        else:
            executor = self.events[self.event]

        return await executor()

    async def init(self):

        sub_component = self.get_sub_component()
        if not sub_component:
            await self.isValidEvent()
            return await self.execute_event()

        controller = self.components[sub_component](self.request, self.state, self.sub_components)
        response = await controller.init()
        return response

    def success_event(self):
        return {
            "status" : True,
            "event": self.event
        }

    def error_event(self, reason):
        return {
            "status": False,
            "event": self.event,
            "reason": reason
        }

    def validate_change(self, data):
        attribute = data.get("attribute")

        value = data.get("value")

        if not attribute:
            raise Exception(self.errors[0])

        if attribute not in self.editable_attributes:
            raise Exception(self.errors[100])

        if not value:
            raise Exception(self.errors[200])

    async def change(self):
        data = await self.request.json()

        try:
            self.validate_change(data)
            setattr(self.component, data["attribute"], int(data["value"]))
        except Exception as e:
            raise Exception(e)

        return {
            "change": True
        }
