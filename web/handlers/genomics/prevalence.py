from .util import transform_prevalence, transform_prevalence_by_location_and_tiime, compute_rolling_mean
from .base import BaseHandler
from tornado     import gen
import pandas as pd
from datetime import timedelta

class PrevalenceByLocationHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_division = self.get_argument("division", None)
        cumulative = self.get_argument("cumulative", None)
        cumulative = True if cumulative == "true" else False
        query = {}
        if query_division == None:
            query = {
                "size": 0,
                "aggs": {
                    "prevalence": {
                        "filter" : {
                            "term" : { "country" : query_country }
                        },
                        "aggs": {
                            "count": {
                                "terms": {
                                    "field": "date_collected",
                                    "size": self.size
                                },
                                "aggs": {
                                    "lineage_count": {
                                        "filter": {
                                            "term" : { "pangolin_lineage" : query_pangolin_lineage }
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        else:
            query = {
                "size": 0,
                "aggs": {
                    "prevalence": {
                        "filter" : {
                            "term" : { "division" : query_division }
                        },
                        "aggs": {
                            "count": {
                                "terms": {
                                    "field": "date_collected",
                                    "size": self.size
                                },
                                "aggs": {
                                    "lineage_count": {
                                        "filter": {
                                            "term" : { "pangolin_lineage" : query_pangolin_lineage }
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "prevalence", "count", "buckets"]
        resp = transform_prevalence(resp, path_to_results, cumulative)
        self.write(resp)

# Most recent prevalence
class PrevalenceByCountryAndTimeHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query = {
            "size": 0,
            "aggs": {
                "country_date_buckets": {
                    "composite": {
                        "size": 10000,
                        "sources": [
                            {"date_collected": { "terms": {"field": "date_collected"}}},
                            {"country": { "terms": {"field": "country"} }}
                        ]
                    },
                    "aggregations": {
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
        ctr = 0
        buckets = resp["aggregations"]["country_date_buckets"]["buckets"]
        # Get all paginated results
        while "after_key" in resp["aggregations"]["country_date_buckets"]:
            query["aggs"]["country_date_buckets"]["composite"]["after"] = resp["aggregations"]["country_date_buckets"]["after_key"]
            resp = yield self.asynchronous_fetch(query)
            buckets.extend(resp["aggregations"]["country_date_buckets"]["buckets"])
        if len(buckets) == 0:
            return {"success": True, "results": []}
        flattened_response = [{
            "date": i["key"]["date_collected"],
            "name": i["key"]["country"],
            "total_count": i["doc_count"],
            "lineage_count": i["lineage_count"]["doc_count"]
        } for i in buckets if len(i["key"]["date_collected"].split("-")) > 1 and "XX" not in i["key"]["date_collected"]]
        dict_response = transform_prevalence_by_location_and_tiime(flattened_response)
        resp = {"success": True, "results": dict_response}
        self.write(resp)

class PrevalenceByDivisionAndTimeHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_country = self.get_argument("country", None)
        query =      {
            "size": 0,
            "query": {
	        "term": {"country": query_country}
            },
            "aggs": {
                "division_date_buckets": {
                    "composite": {
                        "size": 10000,
                        "sources": [
                            {"date_collected": { "terms": {"field": "date_collected"}}},
                            {"division": { "terms": {"field": "division"} }}
                        ]
                    },
                    "aggregations": {
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
        ctr = 0
        buckets = resp["aggregations"]["division_date_buckets"]["buckets"]
        # Get all paginated results
        while "after_key" in resp["aggregations"]["division_date_buckets"]:
            query["aggs"]["division_date_buckets"]["composite"]["after"] = resp["aggregations"]["division_date_buckets"]["after_key"]
            resp = yield self.asynchronous_fetch(query)
            buckets.extend(resp["aggregations"]["division_date_buckets"]["buckets"])
        if len(buckets) == 0:
            return {"success": True, "results": []}
        flattened_response = [{
            "date": i["key"]["date_collected"],
            "name": i["key"]["division"],
            "total_count": i["doc_count"],
            "lineage_count": i["lineage_count"]["doc_count"]
        } for i in buckets if len(i["key"]["date_collected"].split("-")) > 1 and "XX" not in i["key"]["date_collected"]]
        dict_response = transform_prevalence_by_location_and_tiime(flattened_response)
        resp = {"success": True, "results": dict_response}
        self.write(resp)


# 3. Get prevalence of lineage by date
class PrevalenceHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        cumulative = self.get_argument("cumulative", None)
        cumulative = True if cumulative == "true" else False
        query = {
            "size": 0,
            "aggs": {
                "prevalence": {
                    "terms": {
                        "field": "date_collected",
                        "size": self.size
                    },
                    "aggs": {
                        "lineage_count": {
                            "filter": {
                                "term" : {
                                    "pangolin_lineage" : query_pangolin_lineage
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "prevalence", "buckets"]
        resp = transform_prevalence(resp, path_to_results, cumulative)
        self.write(resp)

class PrevalenceAllLineagesByCountryHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query = {
            "size": 0,
            "query": {
                "term" : { "country" : query_country }
            },
            "aggs": {
                "count": {
                    "terms": {
                        "field": "date_collected",
                        "size": self.size
                    },
                    "aggs": {
                        "lineage_count": {
                            "terms": {
                                "field": "pangolin_lineage",
                                "size": self.size
                            }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        buckets = resp
        path_to_results = ["aggregations", "count", "buckets"]
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = []
        for i in buckets:
            if len(i["key"].split("-")) == 1 or "XX" in i["key"]:
                continue
            for j in i["lineage_count"]["buckets"]:
                flattened_response.append({
                    "date": i["key"],
                    "total_count": i["doc_count"],
                    "lineage_count": j["doc_count"],
                    "lineage": j["key"]
                })
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(
                date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"),
                prevalence = lambda x: x["lineage_count"]/x["total_count"]
            )
            .sort_values("date")
        )
        df_response = df_response.groupby("lineage").apply(compute_rolling_mean, "date", "prevalence", "prevalence_rolling")
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        resp = {"success": True, "results": df_response.to_dict(orient="records")}
        self.write(resp)

class PrevalenceAllLineagesByDivisionHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"term" : { "country" : query_country }},
                        {"term" : { "division" : query_division }}
                    ]
                }
            },
            "aggs": {
                "count": {
                    "terms": {
                        "field": "date_collected",
                        "size": self.size
                    },
                    "aggs": {
                        "lineage_count": {
                            "terms": {
                                "field": "pangolin_lineage",
                                "size": self.size
                            }
                        }
                    }
                }
            }
        }
        resp = yield self.asynchronous_fetch(query)
        buckets = resp
        path_to_results = ["aggregations", "count", "buckets"]
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = []
        for i in buckets:
            if len(i["key"].split("-")) == 1 or "XX" in i["key"]:
                continue
            for j in i["lineage_count"]["buckets"]:
                flattened_response.append({
                    "date": i["key"],
                    "total_count": i["doc_count"],
                    "lineage_count": j["doc_count"],
                    "lineage": j["key"]
                })
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
            .sort_values("date")
        )
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        resp = {"success": True, "results": df_response.to_dict(orient="records")}
        self.write(resp)

