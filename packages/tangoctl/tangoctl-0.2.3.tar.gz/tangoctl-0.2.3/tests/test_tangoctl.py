#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

"""Tests for `tangoctl` package."""


import sys

py_xy = sys.version_info[:2]
if py_xy < (3, 0):
    import mock
else:
    from unittest import mock

import pytest

import tango
import tangoctl.tangoctl

IOR = 'IOR:010000001700000049444c3a54616e676f2f4465766963655f353a312e3000000100000000000000a1000000010102000e0000003139322e3136382e34332e35380010270800000064617461626173650300000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100025454413d000000010000000c000000546961676f4c656e6f766f00250000002f746d702f6f6d6e692d74616e676f2f3030303030333231332d3135343238303034313400'

@pytest.fixture
def tango():
    with mock.patch('tango.DeviceProxy') as DeviceProxy, \
         mock.patch('tango.Database') as Database:
        dp = DeviceProxy.return_value
        dp.name.return_value = 'sys/database/2'
        dp.ping.return_value = 546
        dp.DbMySqlSelect.return_value = [
            [1, 0, 1, 1, 1, 1,
             1, 0, 1, 1, 1, 1, 2, 6],
            ['sys/database/2', '', '1', 'acme', 'DataBaseds/2', 'DataBase',
             'sys/tg_test/1', '', '1', 'acme', 'TangoTest/test', 'TangoTest']
        ]
        db = Database.return_value
        db.get_server_list.return_value = ['DataBaseds/2', 'TangoTest/1']
        db.get_db_host.return_value = 'acme'
        db.get_db_port.return_value = 10000
        dev_info = mock.Mock(class_name='DataBase', ds_full_name='DataBaseds/2',
                             exported=1, pid=12345,
                             started_date='21st November 2018 at 12:40:14',
                             stopped_date='', version=5, ior=IOR)
        dev_info.name = 'sys/database/2'
        db.get_device_info.return_value = dev_info
        yield tango
        # todo reset mock


def test_device_list(tango):
    dl = tangoctl.tangoctl.device_list()
    assert dl == 'sys/database/2  sys/tg_test/1'


def test_server_list(tango):
    sl = tangoctl.tangoctl.server_list()
    assert sl == 'DataBaseds/2  TangoTest/1'

    sl = tangoctl.tangoctl.server_list('Tango*')
    assert sl == 'TangoTest/1'


def test_server_tree(tango):
    tree = tangoctl.tangoctl.server_tree()
    tree_lines = tree.split('\n')
    assert tree_lines[0] == 'acme:10000'
    assert 'DataBaseds' in tree_lines[1]
    assert '2' in tree_lines[2]
    assert 'sys/database/2' in tree_lines[3]
    assert 'TangoTest' in tree_lines[4]
    assert 'test' in tree_lines[5]
    assert 'sys/tg_test/1' in tree_lines[6]
    assert len(tree_lines) == 8


def test_device_info(tango):
    info = tangoctl.tangoctl.device_info('sys/database/2')
    assert 'class = DataBase' in info
    assert 'exported = 1' in info
    assert 'pid = 1234' in info
    assert 'name = sys/database/2' in info
    assert 'server = DataBaseds/2' in info


@pytest.mark.skip
def test_device_ping(tango):
    result = list(tangoctl.tangoctl.device_ping('sys/database/2'))
    assert len(result) == 1
    assert result[0] == 'sys/database/2: 546us'


def test_server_ping(tango):
    result = tangoctl.tangoctl.server_ping('DataBaseds/2')
    assert result == 'DataBaseds/2: 546us'


def test_server_info(tango):
    info = tangoctl.tangoctl.server_info('DataBaseds/2')
    assert 'class = DataBase' not in info
    assert 'exported = 1' in info
    assert 'pid = 1234' in info
    assert 'name = DataBaseds/2' in info
