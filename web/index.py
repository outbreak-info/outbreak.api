import sys
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
from tornado.options import define, options

from handlers import APP_LIST

src_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

if src_path not in sys.path:
    sys.path.append(src_path)
print(src_path)

(SRC_PATH, _) = os.path.split(os.path.abspath(__file__))
STATIC_PATH = os.path.join(SRC_PATH,'../templates/static')
print(STATIC_PATH)

define("port", default=8000, help="run on the given port", type=int)
define("address", default="127.0.0.1", help="run on localhost")
define("debug", default=False, type=bool, help="run in debug mode")
tornado.options.parse_command_line()
if options.debug:
    import tornado.autoreload
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    options.address = '0.0.0.0'

settings = {}

if options.debug:
    settings.update({
        "static_path": STATIC_PATH,
    })
    settings.update({"debug": True})

def main():
    application = tornado.web.Application(APP_LIST, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port, address=options.address)
    loop = tornado.ioloop.IOLoop.instance()
    if options.debug:
        tornado.autoreload.start(loop)
        logging.info('Server is running on "%s:%s"...' % (options.address, options.port))
    loop.start()


if __name__ == "__main__":
    main()
