# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import absolute_import

"""
$ tangoctl server list
$ tangoctl server info -s <server>
$ tangoctl server tree [--filter=<filter>]
$ tangoctl server <start>|<stop>|<status> [<server>]+
$ tangoctl server add -s <server> [-d <class> <device>]+
$ tangoctl server delete [<server>]+
$ tangoctl device list
$ tangoctl device tree [--filter=<filter>]
$ tangoctl device add -s <server> [-d <class> <device>]+ (same as "server add")
$ tangoctl device delete [<device>]+
$ tangoctl device info -d <name>
$ tangoctl device command list -d <device> [--filter=<filter>]
$ tangoctl device command exec -d <device> -c <command> [-p <parameter value>]
$ tangoctl device command info -d <device> -c <command>
$ tangoctl device attribute list -d <device> [--filter=<filter>]
$ tangoctl device attribute read -d <device> -a <attribute>
$ tangoctl device attribute write -d <device> -a <attribute> -v <value>
$ tangoctl device attribute info -d <device> -a <attribute>
$ tangoctl device property read -d <device> -a <attribute> -p <property>
$ tangoctl device property write -d <device> -a <attribute> -p <property> -v <value>
"""

import functools

import click

from . import tangoctl


class error(tangoctl.ErrorHandler):
    def __init__(self, verbose=False):
        echo = functools.partial(click.echo, err=True)
        super(error, self).__init__(echo=echo, verbose=verbose)


@click.group()
def cli():
    """Query or send control commands to the tango system

    EXAMPLES

       Display tree of servers:

       $ tangoctl server tree

       Display list of devices:

       $ tangoctl device list

       Read 'state' attribute from a device

       $ tangoctl device attribute read -d sys/tg_test/1 -a state

       Execute command Init() on a device

       $ tangoctl device command exec -d sys/tg_test/1 -c init

       Display 'double_spectrum' attribute information

       $ tangoctl device attribute info -d sys/tg_test/1 -a double_spectrum

       Display list of device attributes:

       $ tangoctl device attribute list -d sys/tg_test/1

    """
    pass


@cli.group('device', help='device related operations')
def device():
    pass


@device.command('list', help='show list of devices')
def device_list():
    with error():
        click.echo(tangoctl.device_list())


@device.command('tree', help='show tree of devices')
@click.option('--filter', default=None, show_default=True,
              help='filter devices (supports pattern matching *,?,[])')
def device_tree(filter):
    with error():
        click.echo(tangoctl.device_tree(filter=filter))


@device.command('ping', help='ping device(s)')
@click.argument('devices', nargs=-1)
def ping(devices):
    with error():
        for result in tangoctl.device_ping(devices):
            click.echo(result)


@device.command('add', help='register new device(s)')
@click.option('-s', '--server', required=True, prompt=True,
              help='server name (<type>/<instance>)')
@click.option('-d', '--device', required=True, multiple=True, type=(str, str),
              help='device class and name ()')
def device_add(server, device):
    """Registers new device(s) in the tango database. Each device must be in
    the format "<class> <name>" where name must follow the usual
    <domain>/<family>/<member>"""
    with error():
        for serv, dev in tangoctl.device_add(server, device):
            click.echo('Registered {} in {}'.format(dev, serv))


@device.command('delete', help='unregisters device(s)')
@click.argument('devices', nargs=-1)
def device_delete(devices):
    with error():
        tangoctl.device_delete(devices)


@device.group('command', help="command related operations")
def device_command():
    pass


@device_command.command('exec', help='execute specified command')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
@click.option('-c', '--command', required=True, prompt=True,
              help='command name')
@click.option('-p', '--parameter', help='command parameter')
def device_command_exec(device, command, parameter):
    with error():
        click.echo(tangoctl.device_command(device, command, parameter))


@device_command.command('list', help='show device commands')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
def device_command_list(device):
    with error():
        click.echo(tangoctl.device_command_list(device))


@device_command.command('info', help='information about a command')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
@click.option('-c', '--command', required=True, prompt=True,
              help='command name')
def device_command_info(device, command):
    with error():
        click.echo(tangoctl.device_command_info(device, command))


@device.group('attribute', help="attribute related operations")
def device_attribute():
    pass


@device_attribute.command('read', help='read device attribute')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
@click.option('-a', '--attribute', required=True, prompt=True,
              help='attribute name')
@click.option('-v', '--verbose', default=False, show_default=True, is_flag=True)
def device_attribute_read(device, attribute, verbose):
    with error():
        click.echo(tangoctl.device_attribute_read(device, attribute,
                                                  verbose=verbose))


@device_attribute.command('write', help='write device attribute')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
@click.option('-a', '--attribute', required=True, prompt=True,
              help='attribute name')
@click.option('-v', '--value', required=True, prompt=True,
              help='value to write')
def device_write(device, attribute, value):
    with error():
        click.echo(tangoctl.device_attribute_write(device, attribute, value))


@device_attribute.command('info', help='information about a device attribute')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
@click.option('-a', '--attribute', required=True, prompt=True,
              help='attribute name')
def device_attribute_info(device, attribute):
    with error():
        click.echo(tangoctl.device_attribute_info(device, attribute))


@device_attribute.command('list', help='show device attributes')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
@click.option('-v', '--verbose', default=False, show_default=True, is_flag=True)
def device_attribute_list(device, verbose):
    with error():
        click.echo(tangoctl.device_attribute_list(device, verbose=verbose))


@device.group('property', help="device property related operations")
def device_property():
    pass


@device_property.command('read', help='read device property')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
@click.option('-p', '--property', required=True, prompt=True,
              help='property name')
def device_property_read(device, property):
    with error():
        click.echo(tangoctl.device_property_read(device, property))


@device_property.command('write', help='write device property')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
@click.option('-p', '--property', required=True, prompt=True,
              help='property name')
@click.option('-v', '--value', required=True, prompt=True,
              help='value to write')
def device_property_write(device, property, value):
    with error():
        click.echo(tangoctl.device_property_write(device, property, value))


@device.command('info', help='information about a device')
@click.option('-d', '--device', required=True, prompt=True,
              help='device name')
def device_info(device):
    with error():
        click.echo(tangoctl.device_info(device))


@cli.group('server', help='server related operations')
def server():
    pass


@server.command('list', help='show list of servers')
@click.option('--filter', default=None, show_default=True,
              help='filter servers (supports pattern matching *,?,[])')
def server_list(filter):
    with error():
        click.echo(tangoctl.server_list(filter=filter))


@server.command('ping', help='ping server')
@click.option('-s', '--server', required=True, prompt=True,
              help='server name (<type>/<instance>)')
def server_ping(server):
    with error():
        click.echo(tangoctl.server_ping(server))


@server.command('add', help='register a new server')
@click.option('-s', '--server', required=True, prompt=True,
              help='server name (<type>/<instance>)')
@click.option('-d', '--device', required=True, multiple=True, type=(str, str),
              help='device class and name')
def server_add(server, device):
    """Registers a new server in the tango database with the given list of
    DEVICES. Each device must be in the format "<class> <name>" where name
    must follow the usual <domain>/<family>/<member>"""
    with error():
        for serv, dev in tangoctl.server_add(server, device):
            click.echo('Registered {} in {}'.format(dev, serv))


@server.command('delete', help='unregister an existing server')
@click.option('-s', '--server', required=True, prompt=True,
              help='server name (<type>/<instance>)')
def server_delete(server):
    with error():
        tangoctl.server_delete(server)


@server.command('info', help='show server information')
@click.option('-s', '--server', required=True, prompt=True,
              help='server name (<type>/<instance>)')
def server_info(server):
    with error():
        click.echo(tangoctl.server_info(server))


@server.command('tree', help='show tree of servers')
@click.option('-c', '--compact', default=False, show_default=True, is_flag=True)
@click.option('--server-only', default=False, show_default=True, is_flag=True)
@click.option('--filter', default=None, show_default=True,
              help='filter servers (supports pattern matching *,?,[])')
def server_tree(compact, server_only, filter):
    tree = tangoctl.server_tree(compact=compact, server_only=server_only,
                                filter=filter)
    click.echo(tree)


if __name__ == '__main__':
    cli()
