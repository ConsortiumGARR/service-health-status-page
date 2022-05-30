import json
from bson import json_util


def mongo_cursor_to_json(mongo_cursor):
    data = [json.loads(json.dumps(id_to_string(item), default=json_util.default))
            for item in mongo_cursor]
    return data


def id_to_string(item):
    item['_id'] = str(item['_id'])
    return item
