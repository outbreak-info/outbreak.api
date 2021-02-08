from .base import BaseHandler
from tornado import gen
import pandas as pd

import re

class LineageByCountryHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query = {
            "aggs": {
                "prevalence": {
                    "filter" : { "term": {"pangolin_lineage": query_pangolin_lineage}},
                    "aggs": {
                        "country": {
	                    "terms": {
                                "field": "country",
                                "size": self.size
                            }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)

class LineageByDivisionHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_country = self.get_argument("country", None)
        query = {
            "aggs": {
                "prevalence": {
                    "filter" : {
                        "bool" : {
                            "must" : [
                                {"term" : { "country" : query_country }},
                                {"term" : { "pangolin_lineage" : query_pangolin_lineage }}
                            ]
                        }
                    },
                    "aggs": {
                        "division": {
	                    "terms": {
                                "field": "division",
                                "size": self.size
                            }
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


# #1. Calculate total number of sequences with a particular lineage at Country
class LineageAndDivisionHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query = {
            "query": {
                "bool" : {
                    "must" : [
                        {"term" : { "country" : query_country }},
                        {"term" : { "pangolin_lineage" : query_pangolin_lineage }},
                        {"term" : { "division" : query_division }}
                    ]
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)

class LineageHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        query_str = self.get_argument("name", None)
        query = {
            "size": 0,
            "query": {
                "wildcard": {
                    "pangolin_lineage": {
                        "value": query_str
                    }
                }
            },
            "aggs": {
                "lineage": {
                    "terms": {
                        "field": "pangolin_lineage",
                        "size": 10000
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "lineage", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{
            "name": i["key"],
            "total_count": i["doc_count"]
        } for i in buckets]
        resp = {"success": True, "results": flattened_response}
        self.write(resp)


class LineageMutationsHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        pangolin_lineage = self.get_argument("pangolin_lineage", None)
        frequency = self.get_argument("frequency", None)
        frequency = float(frequency) if frequency != None else 0.8
        query = {
            "size": 0,
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"pangolin_lineage": pangolin_lineage}}
                    ]
                }
            },
            "aggs": {
                "mutations": {
                    "terms": {
                        "field": "mutations.mutation",
                        "size": 10000
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "mutations", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{
            "mutation": i["key"],
            "mutation_count": i["doc_count"],
            "lineage_count": resp["hits"]["total"]
        } for i in buckets]
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(
                gene = lambda x: x["mutation"].apply(lambda k: k.split(":")[0]),
                ref_aa = lambda x: x["mutation"].apply(lambda k: re.findall("[A-Z]+", k.split(":")[1])[0] if "DEL" not in k and "_" not in k else k),
                alt_aa = lambda x: x["mutation"].apply(lambda k: re.findall("[A-Z]+", k.split(":")[1])[1] if "DEL" not in k and "_" not in k else k.split(":")[1]),
                codon_num = lambda x: x["mutation"].apply(lambda k: re.findall("[0-9]+", k.split(":")[1])[0] if "DEL" not in k and "_" not in k else k.split(":")[1]),
                type = lambda x: x["mutation"].apply(lambda k: "deletion" if "DEL" in k else "substitution")
            )
        )
        df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
        df_response.loc[:, "prevalence"] = df_response["mutation_count"]/df_response["lineage_count"]
        df_response = df_response[df_response["prevalence"] >= frequency]
        resp = {"success": True, "results": df_response.to_dict(orient="records")}
        self.write(resp)

