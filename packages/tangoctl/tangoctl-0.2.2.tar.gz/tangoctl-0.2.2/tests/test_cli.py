#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

from click.testing import CliRunner

from tangoctl.cli import cli

from test_tangoctl import tango

def test_no_args():
    """Test the CLI."""
    result = CliRunner().invoke(cli)
    assert result.exit_code == 0
    assert 'Query or send control commands to the tango system' in result.output


def test_help():
    result = CliRunner().invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert '--help  Show this message and exit.' in result.output


def test_device_list(tango):
    result = CliRunner().invoke(cli, ['device', 'list'])
    assert result.exit_code == 0
    assert result.output.strip() == 'sys/database/2  sys/tg_test/1'


def test_server_list(tango):
    result = CliRunner().invoke(cli, ['server', 'list'])
    assert result.exit_code == 0
    assert result.output.strip() == 'DataBaseds/2  TangoTest/1'


def test_server_ping(tango):
    result = CliRunner().invoke(cli, ['server', 'ping', '-s', 'DataBaseds/2'])
    assert result.exit_code == 0
    assert result.output.strip() == 'DataBaseds/2: 546us'
