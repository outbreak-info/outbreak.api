import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from elasticsearch import AsyncElasticsearch

#4. Count total number of sequences of lineage by country
class LineageByCountryHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query = {
            "aggs": {
                "country": {
                    "filter" : { "term": {"pangolin_lineage": query_pangolin_lineage}},
                    "aggs": {
                        "country": {
	                    "terms": { "field": "country" }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)

# #1. Calculate total number of sequences with a particular lineage at Country
class LineageAndCountryHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query = {
            "query": {
                "bool" : {
                    "must" : [
                        {"term" : { "country" : query_country }},
                        {"term" : { "pangolin_lineage" : query_pangolin_lineage }}
                    ]
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)

# 3. Get prevalence of lineage by date and country
class PrevalenceByCountryHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query = {
            "size": 0,
            "aggs": {
                "country": {
                    "filter" : {
                        "term" : { "country" : query_country }
                    },
                    "aggs": {
                        "count": {
                            "terms": { "field": "date_collected" },
                            "aggs": {
                                "lineage_count": {
                                    "filter": {
                                        "term" : { "pangolin_lineage" : query_pangolin_lineage }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)

# 3. Get prevalence of lineage by date and country
class PrevalenceHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query = {
            "size": 0,
            "aggs": {
                "count": {
                    "terms": { "field": "date_collected" },
                    "aggs": {
                        "lineage_count": {
                            "filter": {
                                "term" : { "pangolin_lineage" : query_pangolin_lineage }
                            }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)

"""
class sitRepApp(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(sitRepApp, self).__init__(*args, **kwargs)

        self.elastic_client = AsyncElasticsearch(hosts=["http://su07:9205/"])

application = sitRepApp(handlers=[
    (r"/api/lineage-by-country", LineageByCountryHandler),
    (r"/api/lineage-and-country", LineageAndCountryHandler),
    (r"/api/prevalence-by-country", PrevalenceByCountryHandler),
    (r"/api/prevalence", PrevalenceHandler),
])

if __name__ == "__main__":
    http_server=tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
"""
