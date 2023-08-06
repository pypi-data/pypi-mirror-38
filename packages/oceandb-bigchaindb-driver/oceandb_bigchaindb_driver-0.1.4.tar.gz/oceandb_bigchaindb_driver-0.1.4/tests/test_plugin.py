#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oceandb_driver_interface.oceandb import OceanDb
from oceandb_driver_interface.search_model import FullTextModel, QueryModel

bdb = OceanDb('./tests/oceandb.ini').plugin


def test_plugin_type_is_bdb():
    assert bdb.type == 'BigchainDB'


def test_plugin_write_and_read():
    bdb.write({"value": "plugin"}, 1)
    assert bdb.read(1)['value'] == 'plugin'
    bdb.delete(1)


def test_update():
    bdb.write({"value": "example"}, 2)
    assert bdb.read(2)['value'] == 'example'
    bdb.update({"value": "testUpdated"}, 2)
    bdb.update({"value": "testUpdated2"}, 2)
    assert bdb.read(2)['value'] == 'testUpdated2'
    bdb.delete(2)


def test_plugin_list():
    bdb.write({"value": "test1"}, 3)
    bdb.update({"value": "testUpdated"}, 3)
    bdb.write({"value": "test2"}, 4)
    bdb.write({"value": "test3"}, 5)
    assert len(bdb.list()) == 3
    assert bdb.list()[0]['value'] == 'testUpdated'
    bdb.delete(3)
    bdb.delete(4)
    bdb.delete(5)
    assert len(bdb.list()) == 0


def test_plugin_query():
    bdb.write({'value': 'bdb'}, 6)
    search_model = QueryModel({'value': 'bdb'}, {'value': -1})
    assert bdb.query(search_model)[0]['value'] == 'bdb'
    bdb.delete(6)


def test_plugin_query_text():
    bdb.write({'key': 'A', 'value': 'test first'}, 7)
    bdb.write({'key': 'B', 'value': 'test second'}, 8)
    bdb.write({'key': 'C', 'value': 'test third'}, 9)
    bdb.write({'key': 'D', 'value': 'test fourth'}, 10)
    search_model = FullTextModel('test', {'key': -1}, offset=3, page=0)
    search_model1 = FullTextModel('test', {'key': -1}, offset=3, page=1)
    assert len(bdb.text_query(search_model)) == 3
    assert bdb.text_query(search_model)[0]['metadata']['data']['key'] == 'D'
    assert bdb.text_query(search_model)[1]['metadata']['data']['key'] == 'C'
    assert bdb.text_query(search_model1)[0]['metadata']['data']['key'] == 'A'
    bdb.delete(7)
    bdb.delete(8)
    bdb.delete(9)
    bdb.delete(10)
