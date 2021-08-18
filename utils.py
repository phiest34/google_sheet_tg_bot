def find(lst: [], searching_item):
    for item in lst:
        if item == searching_item:
            return item


def list_to_dict_indexed(lst):
    return {key: i for i, key in enumerate(lst)}


def index_of(lst, item):
    i = 0
    for list_item in lst:
        if item == list_item:
            return i
        i += 1
    return -1


def starts_with_hash(lst):
    return_items = []
    for i in lst:
        for item in i:
            if item and item[0] == "#":
                return_items.append(item)
    return return_items
