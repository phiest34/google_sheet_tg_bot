import json

def find(lst: [], searching_item):
    for item in lst:
        if item == searching_item:
            return item


def list_to_dict_indexed(lst: []):
    return {key: i for i, key in enumerate(lst)}


def index_of(lst: [], item):
    i = 0
    for list_item in lst:
        if item == list_item:
            return i
        i += 1
    return -1


def starts_with_hash(lst: [str]):
    return_items = []
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] and lst[i][j][0] == "#":
                return_items.append((i, j))
    return return_items


def dict_to_json(dic: {}):
    return json.dumps(dic)


def from_json(string: str):
    return json.loads(string)
