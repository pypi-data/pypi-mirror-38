# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

import json
from datetime import datetime

from tornado.web import RequestHandler, url
from tornado.websocket import WebSocketHandler

from . import app


class route(object):
    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        app.add_handlers(r'.*$', (url(self.url, cls, name=cls.__name__),))
        return cls


@route(r'/')
class Index(RequestHandler):
    def get(self):
        return self.render('index.html')


@route(r'/api/watchers/(?P<watcher_uuid>[0-9a-f-]+)/check_now/')
class CheckNow(RequestHandler):
    async def get(self, watcher_uuid):
        for watchers in app.watchers.values():
            for watcher in watchers:
                if watcher.uuid == watcher_uuid:
                    await watcher.check(replan=False)
                    return self.redirect(
                        self.reverse_url('Watcher', watcher_uuid))
        return self.send_error(404)


@route(r'/websocket')
class WebSocket(WebSocketHandler):
    def open(self):
        app.websockets.append(self)

    def on_close(self):
        app.websockets.remove(self)


@route(r'/api/services/')
class ServicesListApi(RequestHandler):
    async def get(self):
        return self.write({'objects': [
            dict(service) for service in app.services.values()
        ]})


def watcher_to_dict(w):
    return {
        'uuid': w.uuid,
        'server': dict(w.server),
        'service': dict(w.service),
        'status': w.status,
        'last_result': w.last_check_result,
        'description': w.description,
        'next_check_hour': w.next_check_hour,
    }


def watcher_encoder(o):
    if isinstance(o, bytes):
        return o.decode()
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + ' is not json serializable')


@route(r'/api/watchers/')
class WatchersListApi(RequestHandler):
    async def get(self):
        self.write(json.dumps({'objects': [
            watcher_to_dict(w) for l in app.watchers.values() for w in l
        ]}, default=watcher_encoder))
        self.set_header('Content-Type', 'application/json')


@route(r'/api/servers/')
class ServersListApi(RequestHandler):
    async def get(self):
        return self.write({'objects': [dict(s) for s in app.servers.values()]})


def groups_to_dictlist(groups):
    for name, servers in groups.items():
        yield {'name': name, 'members': [server.uuid for server in servers]}


@route(r'/api/groups/')
class GroupsListApi(RequestHandler):
    async def get(self):
        return self.write({'objects': list(groups_to_dictlist(app.groups))})


@route(r'/api/loggers/')
class LoggersListApi(RequestHandler):
    async def get(self):
        return self.write({'objects': [
            {'type': x.type for x in app.loggers}
        ]})
