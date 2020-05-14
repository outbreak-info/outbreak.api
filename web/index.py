from tornado.web import RedirectHandler

from biothings.web.index_base import main

from web.handlers import MainHandler, ApiViewHandler


if __name__ == '__main__':
    extra_app_list = [
        (r"/", MainHandler),
        (r"/v1/(.*)", RedirectHandler, {"url": "/covid19/{0}"}),
        (r"/.+", ApiViewHandler)
    ]
    main(extra_app_list)
