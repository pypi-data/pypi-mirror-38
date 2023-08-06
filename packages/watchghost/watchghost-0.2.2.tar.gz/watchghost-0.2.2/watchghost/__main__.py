#!/usr/bin/env python3

# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

import asyncio
import logging
import os
import sys
from os.path import isfile

from tornado.options import options, parse_command_line, parse_config_file
from tornado.platform.asyncio import AsyncIOMainLoop
from utils import reload
from watchghost import app, config, web  # noqa

DEFAULT_CONFIG = '/etc/watchghost.conf'


def main():
    AsyncIOMainLoop().install()

    watchghost_config = os.environ.get('WATCHGHOST_CONFIG')
    if watchghost_config:
        if not isfile(watchghost_config):
            logging.error('File {} does not exist', watchghost_config)
            sys.exit(1)
        parse_config_file(watchghost_config)
    elif isfile(DEFAULT_CONFIG):
        parse_config_file(DEFAULT_CONFIG)
    else:
        parse_command_line()

    log = logging.getLogger('watchghost')
    log.setLevel(logging.DEBUG if options.debug else logging.ERROR)

    config.read()

    log.debug('Listening to http://%s:%i' % (options.host, options.port))
    app.listen(options.port)
    loop = asyncio.get_event_loop()
    if options.reload or options.debug:
        loop.run_until_complete(reload.start_file_watcher(options))
    loop.run_forever()


if __name__ == '__main__':
    main()
