from biothings.web.launcher import main
from tornado.web import RedirectHandler, StaticFileHandler

from web.handlers import ApiViewHandler, MainHandler, SpecialHandler

if __name__ == "__main__":
    main(
        [
            (r"/", MainHandler),
            (r"/v1/(.*)", RedirectHandler, {"url": "/covid19/{0}"}),
            (r"/try-by-doctype/resources/?", SpecialHandler),
            (r"/try/.+", ApiViewHandler),
            (r"/try/.+/.+", ApiViewHandler),
        ],
        {
            "static_path": "static"
        }
    )  # additionals
