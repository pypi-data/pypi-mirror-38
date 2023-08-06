# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import print_function

import sys
import enum
import fnmatch
import urlparse
import functools
import itertools
import collections

import gevent

import tango.gevent

Database = tango.Database
Device = tango.gevent.DeviceProxy
Attribute = tango.gevent.AttributeProxy

ServerInfo = collections.namedtuple('ServerInfo',
                                    ('name', 'type', 'instance', 'host', 'devices'))
DeviceInfo = collections.namedtuple('DeviceInfo',
                                    ('name', 'server', 'klass', 'alias', 'exported'))
DatabaseInfo = collections.namedtuple('DatabaseInfo',
                                      ('host', 'port', 'servers', 'devices', 'aliases'))


@enum.unique
class TangoType(enum.IntEnum):
    Server = 0
    Database = 1
    Device = 2
    Attribute = 3


def tango_error_str(exc_value, verbose=False):
    if verbose:
        msg = '\n'.join(reversed(['{} @ {}: {}'.format(err.reason,
                                                       err.origin,
                                                       err.desc)
                                  for err in exc_value]))
    else:
        msg = exc_value[0].desc
    return msg


class ErrorHandler(object):

    def build_message(self, exc_type, exc_value, traceback):
        if issubclass(exc_type, tango.DevFailed):
            msg = tango_error_str(exc_value, verbose=self.verbose)
        else:
            msg = str(exc_value)
        return msg

    def __init__(self, echo=None, verbose=False):
        if echo is None:
            echo = functools.partial(print, file=sys.stderr)
        self.echo = echo
        self.verbose = verbose

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            msg = self.build_message(exc_type, exc_value, traceback)
            self.echo(msg)
        return True


_str_like = set((str, bytes))
try:
    _str_like.add(unicode)
except NameError:
    pass
_str_like = tuple(_str_like)


def _url(name_or_url):
    if isinstance(name_or_url, _str_like):
        if name_or_url.startswith('tango://'):
            name_or_url = name_or_url[8:]
        if not ':' in name_or_url:
            db = tango.Database()
            name_or_url = '{}:{}/{}'.format(db.get_db_host(),
                                            db.get_db_port(),
                                            name_or_url)
        name_or_url = 'tango://' + name_or_url
        name_or_url = urlparse.urlparse(name_or_url, allow_fragments=False)
    return name_or_url


def get_tango_type(name):
    url = _url(name)
    path = url.path[1:] if url.path.startswith('/') else url.path
    if not path:
        return TangoType.Database
    if url.netloc:
        host, port = url.netloc.rsplit(':', 1)
        db = tango.Database(host, port)
    else:
        db = tango.Database()
    info = get_db_info(db=db)
    if path in info.aliases or path in info.devices:
        return TangoType.Device
    elif path in info.servers:
        return TangoType.Server
    return TangoType.Attribute


def get_tango_object(name):
    url = _url(name)
    tango_type = get_tango_type(url)
    if tango_type == TangoType.Device:
        obj = Device(name)
    elif tango_type == TangoType.Database:
        host, port = url.netloc.rsplit(':', 1)
        obj = Database(host, port)
    elif tango_type == TangoType.Attribute:
        obj = Attribute(name)
    elif tango_type == TangoType.Server:
        raise NotImplementedError
    return obj, tango_type


def info(name):
    obj, tango_type = get_tango_object(name)
    if tango_type == TangoType.Device:
        msg = obj.info()
    elif tango_type == TangoType.Database:
        msg = obj.get_info()
    elif tango_type == TangoType.Attribute:
        msg = str(obj.get_config())
    elif tango_type == TangoType.Server:
        raise NotImplementedError
    else:
        msg = str(obj)
    return msg


def _db(db=None):
    return tango.Database() if db is None else db


def _db_name(db):
    return '{}:{}'.format(db.get_db_host(), db.get_db_port())


def get_server_devices(server_id, db=None):
    db = _db(db)
    class_list = db.get_device_class_list(server_id)
    return {name: DeviceInfo(name, server_id, klass, alias=None, exported=None)
            for name, klass in zip(class_list[::2], class_list[1::2])}


def _build_db_standard(db=None):
    db = _db(db)
    all_servers, all_devices = {}, {}
    for server_id in db.get_server_list():
        server_type, server_instance = server_id.split('/', 1)
        devices = get_server_devices(server_id, db=db)
        all_devices.update(devices)
        device_names = { device_name for device_name in devices }
        server = ServerInfo(server_id, server_type, server_instance, None,
                            device_names)
        all_servers[server_id] = server
    host, port = db.get_db_host(), db.get_db_port_num()
    return DatabaseInfo(servers=all_servers, devices=all_devices, host=host,
                        port=port, aliases=set())


def _build_db_quick(db_dev):
    all_servers, all_devices = {}, {}
    query = "SELECT name, alias, exported, host, server, class FROM device"
    r = db_dev.DbMySqlSelect(query)
    row_nb, column_nb = r[0][-2:]
    data = r[1]
    assert row_nb == len(data) / column_nb
    all_servers, all_devices, aliases = {}, {}, {}
    for row in range(row_nb):
        idx = row * column_nb
        cells = data[idx:idx + column_nb]
        dev_name, dev_alias, exported, host, server_id, klass = cells
        if not dev_alias:
            dev_alias = None
        else:
            aliases[dev_alias] = dev_name
        device = DeviceInfo(dev_name, server_id, klass, dev_alias,
                            bool(int(exported)))
        server = all_servers.get(server_id)
        if server is None:
            server_type, server_instance = server_id.split('/', 1)
            server = ServerInfo(server_id, server_type, server_instance, host,
                                set())
            all_servers[server_id] = server
        server.devices.add(dev_name)
        all_devices[dev_name] = device
    db = db_dev.get_device_db()
    host, port = db.get_db_host(), db.get_db_port_num()

    return DatabaseInfo(servers=all_servers, devices=all_devices,
                        aliases=aliases, host=host, port=port)


def build_db(db=None):
    db = _db(db)
    db_dev_name = '{}/{}'.format(_db_name(db), db.dev_name())
    db_dev = tango.DeviceProxy(db_dev_name)
    if hasattr(db_dev, 'DbMySqlSelect'):
        return _build_db_quick(db_dev)
    else:
        return _build_db_standard(db=db)

# TODO: consider creating a timestamped ~/.cache/tangoctl/db_name.pkl with db_info

DB_INFO = {}

def get_db_info(db=None):
    global DB_INFO
    db = _db(db)
    db_name = _db_name(db)
    db_info = DB_INFO.get(db_name)
    if db_info is None:
        DB_INFO[db_name] = db_info = build_db(db)
    return db_info


def to_IOR(ior_str):
    if not ior_str.startswith('IOR:'):
        ValueError('Invalid IOR')
    ior_str = ior_str[4:]
    size = len(ior_str) / 2
    for idx in range(size):
        j = 2 * idx
        c = ior_str[j]
        if c >= '0' and c < '9':
            pass
    raise NotImplementedError

def hr_ior(ior):
    raise NotImplementedError

# -----

def server_list(filter=None, db=None):
    db = _db(db)
    servers = db.get_server_list()
    if filter:
        filter = filter.lower()
        servers = (s for s in servers if fnmatch.fnmatch(s.lower(), filter))
    servers = sorted(servers)
    server_rows = _ls_columns(servers)
    return _table(server_rows)


def server_info(name, db=None):
    dserver = 'dserver/' + name
    r = _device_info(dserver, db=db)
    r.pop('class')
    r.pop('server')
    r['name'] = name
    templ = '{{:>{}}} = {{}}'.format(max(map(len, r)))
    lines = [templ.format(name, r[name]) for name in sorted(r)]
    return '\n'.join(lines)


def server_ping(name):
    dserver = 'dserver/' + name
    return _ping(tango.DeviceProxy(dserver))


def server_add(server, devices, db=None):
    db = _db(db)
    for dev_class, dev_name in devices:
        dev_info = tango.DbDevInfo()
        dev_info.name = dev_name
        dev_info._class = dev_class
        dev_info.server = server
        db.add_device(dev_info)
        yield server, '{}:{}'.format(dev_class, dev_name)


def server_delete(server, db=None):
    db = _db(db)
    db.delete_server(server)


def server_tree(db=None, compact=False, server_only=False, filter=None):
    db = _db(db)
    db_info = get_db_info(db=db)
    db_name = _db_name(db)

    import treelib
    tree = treelib.Tree()
    db_node = tree.create_node(db_name)

    servers = db_info.servers
    if filter:
        filter = filter.lower()
        servers = (s for s in servers if fnmatch.fnmatch(s.lower(), filter))

    if compact:
        for serv_name in sorted(servers):
            server = db_info.servers[serv_name]
            serv_inst_node = tree.create_node(serv_name, parent=db_node)
            if not server_only:
                for device in sorted(server.devices):
                    tree.create_node(device, parent=serv_inst_node)
    else:
        # group servers by type
        serv_map = collections.defaultdict(dict)
        for serv_name in servers:
            server = db_info.servers[serv_name]
            serv_map[server.type][server.instance] = server

        for serv_type in sorted(serv_map):
            instances = serv_map[serv_type]
            serv_type_node = tree.create_node(serv_type, parent=db_node)
            for serv_inst in sorted(instances):
                server = instances[serv_inst]
                serv_inst_node = tree.create_node(serv_inst, parent=serv_type_node)
                if not server_only:
                    for device in sorted(server.devices):
                        tree.create_node(device, parent=serv_inst_node)
    return tree


def device_list(db=None):
    db = _db(db)
    info = get_db_info(db=db)
    devices = sorted(info.devices)
    device_rows = _ls_columns(devices, nb_cols=2)
    return _table(device_rows)


def device_tree(db=None, filter=None):
    db = _db(db)
    db_info = get_db_info(db=db)
    db_name = _db_name(db)

    import treelib
    tree = treelib.Tree()
    db_node = tree.create_node(db_name)

    devices = db_info.devices
    if filter:
        filter = filter.lower()
        devices = (d for d in devices if fnmatch.fnmatch(d.lower(), filter))

    domains = collections.defaultdict(functools.partial(collections.defaultdict,
                                                        list))
    for device in devices:
        d, f, m = device.split('/')
        domains[d.lower()][f.lower()].append(m.lower())
    for domain in sorted(domains):
        d_node = tree.create_node(domain, parent=db_node)
        families = domains[domain]
        for family in sorted(families):
            f_node = tree.create_node(family, parent=d_node)
            for member in families[family]:
                tree.create_node(member, parent=f_node)
    return tree


device_add = server_add


def device_delete(devices, db=None):
    db = _db(db)
    for device in devices:
        db.delete_device(str(device))


def _ping(d):
    try:
        msg = '{}us'.format(d.ping())
    except Exception as e:
        msg = tango_error_str(e)
    return '{}: {}'.format(d.name(), msg)


def device_ping(device_names):
    dev_tasks = [gevent.spawn(Device, name) for name in device_names]
    ping_tasks = [gevent.spawn(_ping, task.get())
                  for task in gevent.iwait(dev_tasks)]
    for task in gevent.iwait(ping_tasks):
        yield task.get()


def device_command(name, command, arg):
    device = tango.DeviceProxy(name)
    return str(device.command_inout(command))


def device_attribute_read(name, attribute, verbose=False):
    device = tango.DeviceProxy(name)
    r = device.read_attribute(attribute)
    return str(r if verbose else r.value)


def device_attribute_write(name, attribute, value):
    device = tango.DeviceProxy(name)
    attr_info = device.get_attribute_config(attribute)
    if attr_info.data_type != tango.CmdArgType.DevString:
        value = eval(value)
    device.write_attribute(attribute, value)


def device_attribute_info(name, attribute):
    device = tango.DeviceProxy(name)
    attr_info = device.get_attribute_config(attribute)
    return str(attr_info)


def _device_info(name, db=None):
    db = _db(db)
    info = db.get_device_info(name)
    r = {'class':info.class_name, 'server':info.ds_full_name,
         'exported':info.exported,'name':info.name, 'pid':info.pid,
         'last started':info.started_date, 'last stopped':info.stopped_date,
         'version': info.version}
    if info.exported:
        dinfo = tango.DeviceProxy(name).info()
        r['type'] = dinfo.dev_type
        r['host'] = dinfo.server_host
    return r


def device_info(name, db=None):
    r = _device_info(name, db=db)
    templ = '{{:>{}}} = {{}}'.format(max(map(len, r)))
    lines = [templ.format(name, r[name]) for name in sorted(r)]
    return '\n'.join(lines)


def _ls_columns(seq, nb_cols=4):
    it = iter(seq)
    nb_rows = len(seq) / nb_cols
    pars = nb_rows * (it,)
    return zip(*itertools.izip_longest(*pars, fillvalue=''))


def _obj_members(obj, filter=None, name_suffix=':'):
    if filter is None:
        filter = lambda n: True
    return [(name+name_suffix, getattr(obj, name)) for name in dir(obj)
            if not name.startswith('_') and filter(name)]


def _table(*args, **kwargs):
    import tabulate
    kwargs.setdefault('disable_numparse', True)
    kwargs.setdefault('tablefmt', 'plain')
    return tabulate.tabulate(*args, **kwargs)


def device_attribute_list(dev_name, filter=None, verbose=False):
    device = tango.DeviceProxy(dev_name)
    if filter:
        filter = filter.lower()
        def filt(attr): fnmatch.fnmatch(attr.lower(), filter)
    else:
        filt = lambda x: True
    attrs = {attr.name:attr for attr in device.attribute_list_query_ex()
             if filt(attr.name)}
    lines = []
    for attr_name in sorted(attrs):
        attr = attrs[attr_name]
        lines.append((attr_name,
                      _type_str(tango.CmdArgType.values[attr.data_type]),
                      str(attr.data_format),
                      str(attr.writable)))
    return _table(lines)


def _type_str(t):
    return str(t).replace('Dev', '').replace('Var', '')


def device_command_list(dev_name, filter=None, verbose=False):
    device = tango.DeviceProxy(dev_name)
    if filter:
        filter = filter.lower()
        def filt(cmd): fnmatch.fnmatch(cmd.lower(), filter)
    else:
        filt = lambda x: True
    cmds = {cmd.cmd_name:cmd for cmd in device.get_command_config()
            if filt(cmd.cmd_name)}
    lines = []
    for cmd_name in sorted(cmds):
        cmd = cmds[cmd_name]
        if cmd.in_type != tango.CmdArgType.DevVoid:
            arg = _type_str(cmd.in_type)
        else:
            arg = ''
        if cmd.out_type != tango.CmdArgType.DevVoid:
            res = ' -> ' + _type_str(cmd.out_type)
        else:
            res = ''
        lines.append('{}({}){}'.format(cmd_name, arg, res))
    return '\n'.join(lines)


def device_command_info(name, command):
    device = tango.DeviceProxy(name)
    cmd_info = device.get_command_config(command)
    return str(cmd_info)


def device_property_read(dev_name, property, db=None):
    db = _db(db)
    return db.get_device_property(dev_name, str(property))[property]


def device_property_write(dev_name, property, value, db=None):
    db = _db(db)
    return db.put_device_property(dev_name, {str(property):str(value)})


def handle_request(sock, addr):
    print('client connected', addr)
    file_obj = sock.makefile(mode="rb")
    while True:
        line = file_obj.readline()
        if not line:
            print('client disconnected', addr)
            sock.close()
            return
        line = line.strip()
        if not line:
            continue
        else:
            try:
                r = eval(line)
            except Exception as e:
                r = str(e)
            sock.sendall(bytes(r))


def server():
    import gevent.server
    server = gevent.server.StreamServer(('127.0.0.1', 10010), handle_request)
    print('Ready to accept request')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Ctrl-C hit. Bailing out')

if __name__ == '__main__':
    server()
