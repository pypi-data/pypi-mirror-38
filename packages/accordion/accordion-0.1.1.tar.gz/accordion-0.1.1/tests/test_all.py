from unittest import TestCase

from accordion import compress, expand


class FlatTestCase(TestCase):
    def test_compress(self):
        _compressed = {"data__item*0": 1, "data__item*1": 2, "data__item*2": 3}
        _ex_normal = compress({"data": {"item": [1, 2, 3]}}, node_delimiter="__", list_delimiter="*")
        assert _compressed == _ex_normal

    def test_expand(self):
        _compressed = {"data__item*0": 1, "data__item*1": 2, "data__item*2": 3}
        _normal = {"data": {"item": [1, 2, 3]}}
        _ex_compressed = expand(_compressed, node_delimiter="__", list_delimiter="*")
        assert _normal == _ex_compressed

    def test_both(self):
        _source = {"data": {"item": [1, 2, 3]}}
        _modified = compress(_source, node_delimiter="__", list_delimiter="*")
        _like_source = expand(_modified, node_delimiter="__", list_delimiter="*")
        assert _source == _like_source
