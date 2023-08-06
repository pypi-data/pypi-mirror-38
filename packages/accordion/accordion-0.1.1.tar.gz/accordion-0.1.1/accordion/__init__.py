import collections
from queue import Queue


def compress(data, node_delimiter=".", list_delimiter="/"):
    """
      Turn normal dict into flat with BFS-like queue
    :param data: dict to update
    :param node_delimiter: delimiter which split keys to nodes. For example:
      `{ 'mongo': { 'is': { 'awesome': True } } }` -> `{ 'mongo__is__awesome': True }`
    :param list_delimiter: delimiter which split keys to nodes and list indexes. For example:
      `{ 'mongo': ['is', 'awesome'] }` -> `{ 'mongo*0': 'is', 'mongo*1': 'awesome' }`
    :return: flat dict
    """

    if not isinstance(data, collections.Mapping):
        raise TypeError("Root data must have `dict` type")

    _flat = {}
    _queue = Queue()
    _queue.put(("", data))

    while not _queue.empty():
        _parent_name, _data = _queue.get()

        if isinstance(_data, collections.Mapping):
            for key, value in _data.items():
                _name = f"{_parent_name}{node_delimiter}" if _parent_name else ""

                _queue.put((f"{_name}{key}", value))

        elif isinstance(_data, (tuple, list)):
            for index, value in enumerate(_data):
                _queue.put((f"{_parent_name}{list_delimiter}{index}", value))
        else:
            _flat[f"{_parent_name}"] = _data

    return _flat


def _update_tree(root, nodes, data, list_delimiter):
    _head, *_tail = nodes
    _index = -1

    if list_delimiter in _head:
        _head, _index = _head.split(list_delimiter)
        _index = int(_index)

    if root.get(_head) is None and _index > -1:
        root[_head] = []
    elif root.get(_head) is None and not _tail:
        root[_head] = data
        return
    elif root.get(_head) is None:
        root[_head] = {}

    if isinstance(root.get(_head), dict) and _tail:
        _update_tree(root[_head], _tail, data, list_delimiter)
    elif isinstance(root.get(_head), list):
        while len(root[_head]) < _index + 1:
            root[_head].append(None)

        if _tail:
            _next = {}
            _update_tree(_next, _tail, data, list_delimiter)
            root[_head][_index] = _next
        else:
            root[_head][_index] = data


def expand(data, node_delimiter: str = ".", list_delimiter: str = "/"):
    """
      Turn flat dict into normal
    :param data: dict with flat keys
    :param node_delimiter: delimiter which split keys to nodes. For example:
      `{ 'mongo__is__awesome': True }` -> `{ 'mongo': { 'is': { 'awesome': True } } }`
    :param list_delimiter: delimiter which split keys to nodes and list indexes. For example:
      `{ 'mongo*0': 'is', 'mongo*1': 'awesome' }` -> `{ 'mongo': ['is', 'awesome'] }`
    :return: updated dict
    """
    if not isinstance(data, collections.Mapping):
        raise TypeError("Root data must have `Mapping` type")

    _tree = {}

    for _key, _value in data.items():
        _nodes = _key.split(node_delimiter)
        _update_tree(_tree, _nodes, _value, list_delimiter)

    return _tree


__all__ = [
    'compress',
    'expand'
]
