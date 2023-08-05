import ast
import json


class Json:
    def to(self, obj):
        obj = ast.literal_eval(obj)
        return json.dumps(obj)
