from tornado.web import RedirectHandler

from biothings.web.index_base import main

from web.handlers import MainHandler, ApiViewHandler


if __name__ == '__main__':
    main(app_handlers=[
        (r"/", MainHandler),
        (r"/v1/(.*)", RedirectHandler, {"url": "/covid19/{0}"}),
        (r"/try/.+", ApiViewHandler),
        (r"/try/.+/.+", ApiViewHandler)
    ]) # additionals
