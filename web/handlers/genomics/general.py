import pandas as pd
from .base import BaseHandler
from tornado import gen
from .util import create_nested_mutation_query

class MostRecentDateBase(BaseHandler):
    field = "date_collected"

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query_mutations = self.get_argument("mutations", None)
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query = {
            "size": 0,
            "query": {},
            "aggs": {
                "date_collected": {
                    "terms": {
                        "field": self.field,
                        "size": 10000
                    }
                }
            }
        }
        query_obj = create_nested_mutation_query(country = query_country, division = query_division, lineage = query_pangolin_lineage, mutations = query_mutations)
        query["query"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        print(resp)
        path_to_results = ["aggregations", "date_collected", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        if len(buckets) == 0:
            return {"success": True, "results": []}
        flattened_response = []
        for i in buckets:
            if len(i["key"].split("-")) == 1 or "XX" in i["key"]:
                continue
            flattened_response.append({
                "date": i["key"],
                "date_count": i["doc_count"]
            })
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(
                date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"),
                date_count = lambda x: x["date_count"].astype(int)
            )
            .sort_values("date")
        )
        df_response = df_response.iloc[-1]
        df_response.loc["date"] = df_response["date"].strftime("%Y-%m-%d")
        df_response.loc["date_count"] = int(df_response["date_count"])
        dict_response = df_response.to_dict()
        resp = {"success": True, "results": dict_response}
        self.write(resp)

class MostRecentCollectionDate(MostRecentDateBase):
    field = "date_collected"

class MostRecentSubmissionDate(MostRecentDateBase):
    field = "date_submitted"

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

class MetadataHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.write(self.web_settings.connections.client.indices.get_mapping()['outbreak-genomics']['mappings']['genomics']['_meta'])
