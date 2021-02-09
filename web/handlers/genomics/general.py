import pandas as pd
from .base import BaseHandler
from tornado import gen

class MostRecentCollectionDate(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query = {
            "size": 0,
            "aggs": {
                "lineage_count": {
                    "terms": {
                        "field": "pangolin_lineage",
                        "size": 10000
                    },
                    "aggs": {
                        "date_collected": {
                            "terms": {
                                "field": "date_collected",
                                "size": 10000
                            }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "lineage_count", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        if len(buckets) == 0:
            return {"success": True, "results": []}
        flattened_response = []
        for i in buckets:
            if i["key"] == "None" or i["key"] == "NA":
                continue
            for j in i["date_collected"]["buckets"]:
                if len(j["key"].split("-")) == 1 or "XX" in j["key"]:
                    continue
                flattened_response.append({
                    "date": j["key"],
                    "date_count": j["doc_count"],
                    "total_count": i["doc_count"],
                    "pangolin_lineage": i["key"]
                })
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
            .sort_values("date")
        )
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        if query_pangolin_lineage is not None:
            df_response = df_response[df_response["pangolin_lineage"] == query_pangolin_lineage.lower()]
        df_response = df_response.groupby(["pangolin_lineage"]).nth(-1)
        dict_response = df_response.reset_index().to_dict(orient="records")
        resp = {"success": True, "results": dict_response}
        self.write(resp)

class CountryHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_str = self.get_argument("name", None)
        query = {
            "size": 0,
            "query": {
                "wildcard": {
                    "country": {
                        "value": query_str
                    }
                }
            },
            "aggs": {
                "country": {
                    "terms": {
                        "field": "country",
                        "size": 10000
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "country", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{
            "name": i["key"],
            "total_count": i["doc_count"]
        } for i in buckets]
        resp = {"success": True, "results": flattened_response}
        self.write(resp)

class DivisionHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_str = self.get_argument("name", None)
        query = {
            "size": 0,
            "query": {
                "wildcard": {
                    "division": {
                        "value": query_str
                    }
                }
            },
            "aggs": {
                "division": {
                    "terms": {
                        "field": "division",
                        "size": 10000
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "division", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{
            "name": i["key"],
            "total_count": i["doc_count"]
        } for i in buckets]
        resp = {"success": True, "results": flattened_response}
        self.write(resp)


