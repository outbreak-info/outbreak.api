from biothings.web.launcher import main
from tornado.web import RedirectHandler, StaticFileHandler

from web.handlers import ApiViewHandler, MainHandler, SpecialHandler
from web.handlers.genomics import routes as genomics_routes
from web.handlers.v2.genomics import routes as genomics_v2_routes

if __name__ == '__main__':
    main([
        *genomics_routes,
        *genomics_v2_routes,
        (r"/", MainHandler),
        (r"/static/(.*)", StaticFileHandler, {"path": "./static"}),
        (r"/v1/(.*)", RedirectHandler, {"url": "/covid19/{0}"}),
        (r"/try-by-doctype/resources/?", SpecialHandler),
        (r"/try/.+", ApiViewHandler),
        (r"/try/.+/.+", ApiViewHandler)
    ])  # additionals
