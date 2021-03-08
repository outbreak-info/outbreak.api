import pandas as pd
from .base import BaseHandler
from tornado import gen
from .util import create_nested_mutation_query

class SequenceCountHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query_county = self.get_argument("county", None)
        query_cumulative = self.get_argument("cumulative", None)
        query_cumulative = True if query_cumulative == "true" else False
        if query_cumulative:
            query = {}
            resp = yield self.asynchronous_fetch_count(query)
            flattened_response = {
                "name": "global",
                "total_count": resp["count"]
            }
        else:
            query = {
                "size": 0,
                "aggs": {
                    "country": {
                        "terms": {
                            "field": "country",
                            "size": 10000
                        }
                    }
                }
            }
            if query_county is not None:
                query["query"] = {
                    "match": {
                        "location": query_county
                    }
                }
                query["aggs"]["country"]["terms"]["field"] = "location"
            elif query_division is not None:
                query["query"] = {
                    "match": {
                        "division": query_division
                    }
                }
                query["aggs"]["country"]["terms"]["field"] = "division"
            elif query_country is not None:
                query["query"] = {
                    "match": {
                        "country": query_country
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

class MostRecentDateBase(BaseHandler):
    field = "date_collected"
    location_type = None

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_location = self.get_argument("name", None)
        # query_country = self.get_argument("country", None)
        # query_division = self.get_argument("division", None)
        # query_county = self.get_argument("county", None)
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
        kwargs = {}
        if self.location_type is not None:
            kwargs = {self.location_type: query_location}
        query_obj = create_nested_mutation_query(lineage = query_pangolin_lineage, mutations = query_mutations, **kwargs)
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

class MostRecentCollectionDateGlobalHandler(MostRecentDateBase):
    field = "date_collected"
    location_type = None

class MostRecentCollectionDateByCountryHandler(MostRecentDateBase):
    field = "date_collected"
    location_type = "country"

class MostRecentCollectionDateByDivisionHandler(MostRecentDateBase):
    field = "date_collected"
    location_type = "division"

class MostRecentCollectionDateByCountyHandler(MostRecentDateBase):
    field = "date_collected"
    location_type = "location"

class MostRecentSubmissionDateGlobalHandler(MostRecentDateBase):
    field = "date_submitted"
    location_type = None

class MostRecentSubmissionDateByCountryHandler(MostRecentDateBase):
    field = "date_submitted"
    location_type = "country"

class MostRecentSubmissionDateByDivisionHandler(MostRecentDateBase):
    field = "date_submitted"
    location_type = "division"

class MostRecentSubmissionDateByCountyHandler(MostRecentDateBase):
    field = "date_submitted"
    location_type = "location"



class LocationHandler(BaseHandler):

    location_type = "country"

    @gen.coroutine
    def get(self):
        query_str = self.get_argument("name", None)
        query = {
            "size": 0,
            "query": {
                "wildcard": {
                    "{}_lower".format(self.location_type): {
                        "value": query_str
                    }
                }
            },
            "aggs": {
                "location_code_buckets": {
                    "composite": {
                        "size": self.size,
                        "sources": [
                            {
                                "location": {
                                    "terms": {
                                        "field": self.location_type
                                    }
                                }
                            },
                            {
                                "location_id": {
                                    "terms": {
                                        "field": "{}_id".format(self.location_type)
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
        if self.location_type == "division": # For division add country_name
            query["aggs"]["location_code_buckets"]["composite"]["sources"].append({
                "country": {
                    "terms": {
                        "field": "country"
                    }
                }
            })
            query["aggs"]["location_code_buckets"]["composite"]["sources"].append({
                "country_id": {
                    "terms": {
                        "field": "country_id"
                    }
                }
            })
        elif self.location_type == "location":
            query["aggs"]["location_code_buckets"]["composite"]["sources"].append({
                "country": {
                    "terms": {
                        "field": "country"
                    }
                }
            })
            query["aggs"]["location_code_buckets"]["composite"]["sources"].append({
                "country_id": {
                    "terms": {
                        "field": "country_id"
                    }
                }
            })
            query["aggs"]["location_code_buckets"]["composite"]["sources"].append({
                "division": {
                    "terms": {
                        "field": "division"
                    }
                }
            })
            query["aggs"]["location_code_buckets"]["composite"]["sources"].append({
                "division_id": {
                    "terms": {
                        "field": "division_id"
                    }
                }
            })
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "location_code_buckets", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = []
        if self.location_type == "country":
            flattened_response = [{
                "name": i["key"]["location"],
                "location_id": i["key"]["location_id"],
                "total_count": i["doc_count"]
            } for i in buckets]
        elif self.location_type == "division":
            flattened_response = [{
                "name": i["key"]["location"],
                "location_id": i["key"]["location_id"],
                "country_name": i["key"]["country"],
                "country_id": i["key"]["country_id"],
                "total_count": i["doc_count"]
            } for i in buckets]
        elif self.location_type == "county":
            flattened_response = [{
                "name": i["key"]["location"],
                "location_id": i["key"]["location_id"],
                "country_name": i["key"]["country"],
                "country_id": i["key"]["country_id"],
                "division_name": i["key"]["division"],
                "division_id": i["key"]["division_id"],
                "total_count": i["doc_count"]
            } for i in buckets]
        resp = {"success": True, "results": flattened_response}
        self.write(resp)

class CountryHandler(LocationHandler):
    location_type="country"

class DivisionHandler(LocationHandler):
    location_type="division"

class CountyHandler(LocationHandler):
    location_type="location"

class MutationHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_str = self.get_argument("name", None)
        query = {
            "size": 0,
            "aggs": {
                "mutations": {
                    "nested": {
                        "path": "mutations"
                    },
                    "aggs": {
                        "mutation_filter": {
                            "filter": {
                                "wildcard": {
                                    "mutations.mutation": {
                                        "value": query_str
                                    }
                                }
                            },
                            "aggs": {
                                "count_filter": {
                                    "terms": {
                                        "field": "mutations.mutation",
                                        "size": 10000
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "mutations", "mutation_filter", "count_filter", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{
            "name": i["key"],
            "total_count": i["doc_count"]
        } for i in buckets]
        resp = {"success": True, "results": flattened_response}
        self.write(resp)

class SubmissionLagHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query = {
            "aggs": {
                "date_collected_submitted_buckets": {
                    "composite": {
                        "size": 10000,
                        "sources": [
                            {"date_collected": { "terms": {"field": "date_collected"}}},
                            {"date_submitted": { "terms": {"field": "date_submitted"} }}
                        ]
                    }
                }
            }
        }
        if query_division is not None:
            query["query"] = {
                "match": {
                    "division": query_division
                }
            }
        if query_country is not None:
            query["query"] = {
                "match": {
                    "country": query_country
                }
            }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "date_collected_submitted_buckets", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        while "after_key" in resp["aggregations"]["date_collected_submitted_buckets"]:
            query["aggs"]["date_collected_submitted_buckets"]["composite"]["after"] = resp["aggregations"]["date_collected_submitted_buckets"]["after_key"]
            resp = yield self.asynchronous_fetch(query)
            buckets.extend(resp["aggregations"]["date_collected_submitted_buckets"]["buckets"])
        flattened_response = [{
            "date_collected": i["key"]["date_collected"],
            "date_submitted": i["key"]["date_submitted"],
            "total_count": i["doc_count"]
        } for i in buckets]
        resp = {"success": True, "results": flattened_response}
        self.write(resp)

class MetadataHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.write(self.web_settings.connections.client.indices.get_mapping()['outbreak-genomics']['mappings']['mutation']['_meta'])
