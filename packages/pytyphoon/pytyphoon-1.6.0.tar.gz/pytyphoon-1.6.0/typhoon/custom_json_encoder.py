import json
from bson import json_util

class CustomEncoder(json.JSONEncoder):
    """that's needed for dumping a dict with byte values also"""
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode()
        return json.JSONEncoder.default(self, obj)