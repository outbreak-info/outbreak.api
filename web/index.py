from tornado.web import RedirectHandler

from biothings.web.index_base import main

from web.handlers import MainHandler, ApiViewHandler, SpecialHandler

from web.handlers.genomics import LineageByCountryHandler, LineageAndCountryHandler, PrevalenceByCountryHandler, PrevalenceHandler


if __name__ == '__main__':
    main(app_handlers=[
        (r"/genomics/lineage-by-country",    LineageByCountryHandler),
        (r"/genomics/lineage-and-country",   LineageAndCountryHandler),
        (r"/genomics/prevalence-by-country", PrevalenceByCountryHandler),
        (r"/genomics/prevalence",            PrevalenceHandler),

        (r"/", MainHandler),
        (r"/v1/(.*)", RedirectHandler, {"url": "/covid19/{0}"}),
        (r"/try-by-doctype/resources/?", SpecialHandler),
        (r"/try/.+", ApiViewHandler),
        (r"/try/.+/.+", ApiViewHandler)
    ]) # additionals
