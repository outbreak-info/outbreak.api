import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from elasticsearch import AsyncElasticsearch
import pandas as pd
from datetime import timedelta
from scipy.stats import beta
import re

class sitRepApp(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(sitRepApp, self).__init__(*args, **kwargs)

        self.elastic_client = AsyncElasticsearch(hosts=["http://su07:9205/"])

application = sitRepApp(handlers=[
    (r"/api/lineage-by-country", LineageByCountryHandler),
    (r"/api/lineage-by-division", LineageByDivisionHandler),
    (r"/api/lineage-and-country", LineageAndCountryHandler),
    (r"/api/lineage-and-division", LineageAndDivisionHandler),
    (r"/api/prevalence-by-location", PrevalenceByLocationHandler),
    (r"/api/prevalence-by-country-all-lineages", PrevalenceAllLineagesByCountryHandler),
    (r"/api/prevalence-by-division-all-lineages", PrevalenceAllLineagesByDivisionHandler),
    (r"/api/global-prevalence", PrevalenceHandler),
    (r"/api/lineage-by-country-most-recent", PrevalenceByCountryAndTimeHandler),
    (r"/api/lineage-by-division-most-recent", PrevalenceByDivisionAndTimeHandler),
    (r"/api/most-recent-collection-date", MostRecentCollectionDate),
    (r"/api/country", CountryHandler),
    (r"/api/lineage", LineageHandler),
    (r"/api/division", DivisionHandler),
    (r"/api/lineage-mutations", LineageMutationsHandler)
])

if __name__ == "__main__":
    http_server=tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
