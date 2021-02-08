from tornado.web import RedirectHandler

from biothings.web.index_base import main

from web.handlers import MainHandler, ApiViewHandler, SpecialHandler

from web.handlers.genomics import routes as genomics_routes

if __name__ == '__main__':
    app_handlers = [
        *genomics_routes,
        (r"/", MainHandler),
        (r"/v1/(.*)", RedirectHandler, {"url": "/covid19/{0}"}),
        (r"/try-by-doctype/resources/?", SpecialHandler),
        (r"/try/.+", ApiViewHandler),
        (r"/try/.+/.+", ApiViewHandler)
    ]
    main(app_handlers=app_handlers) # additionals
