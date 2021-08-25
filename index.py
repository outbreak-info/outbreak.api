from biothings.web.launcher import main
from tornado.web import RedirectHandler

from web.handlers import ApiViewHandler, MainHandler, SpecialHandler
from web.handlers.genomics import routes as genomics_routes

if __name__ == '__main__':
    main([
        *genomics_routes,
        (r"/", MainHandler),
        (r"/v1/(.*)", RedirectHandler, {"url": "/covid19/{0}"}),
        (r"/try-by-doctype/resources/?", SpecialHandler),
        (r"/try/.+", ApiViewHandler),
        (r"/try/.+/.+", ApiViewHandler)
    ])  # additionals
