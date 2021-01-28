from tornado import gen

from biothings.web.handlers import BaseHandler as BiothingsBaseHandler

class BaseHandler(BiothingsBaseHandler):
    async def asynchronous_fetch(self, query):
        response = await self.web_settings.connections.async_client.search(
            index = "genomics_parser_20210126_full",
            body = query,
            size = 0
        )
        return response

    def post(self):
        pass

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
