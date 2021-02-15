from .base import BaseHandler
from tornado import gen
import pandas as pd
from .util import create_nested_mutation_query

import re

class LineageByCountryHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_mutations = self.get_argument("mutations", None)
        query = {
            "aggs": {
                "prevalence": {
                    "filter" : {},
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
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query_obj = create_nested_mutation_query(lineage = query_pangolin_lineage, mutations = query_mutations)
        query["aggs"]["prevalence"]["filter"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)

class LineageByDivisionHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_country = self.get_argument("country", None)
        query_mutations = self.get_argument("mutations", None)
        query = {
                "aggs": {
                    "prevalence": {
                        "filter" : {},
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
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query_obj = create_nested_mutation_query(country = query_country, lineage = query_pangolin_lineage, mutations = query_mutations)
        query["aggs"]["prevalence"]["filter"] = query_obj
        print(query)
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)

# Calculate total number of sequences with a particular lineage in a country
class LineageAndCountryHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_mutations = self.get_argument("mutations", None)
        query = {
                "query": {}
        }
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query_obj = create_nested_mutation_query(country = query_country, lineage = query_pangolin_lineage, mutations = query_mutations)
        query["query"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        self.write(resp)


# Calculate total number of sequences with a particular lineage in a division
class LineageAndDivisionHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_mutations = self.get_argument("mutations", None)
        query = {
                "query": {}
        }
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query_obj = create_nested_mutation_query(country = query_country, division = query_division, lineage = query_pangolin_lineage, mutations = query_mutations)
        query["query"] = query_obj
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
                        "nested": {
                            "path": "mutations"
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
                    }
                }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "mutations", "mutations", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{
            "mutation": i["key"],
            "mutation_count": i["doc_count"],
            "lineage_count": resp["hits"]["total"]
            } for i in buckets]
        dict_response = []
        if len(flattened_response) > 0:
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
            dict_response = df_response.to_dict(orient="records")
        resp = {"success": True, "results": dict_response}
        self.write(resp)


class MutationDetailsHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        mutations = self.get_argument("mutations", None)
        mutations = mutations.split(",") if mutations is not None else []
        query = {
            "size": 0,
            "aggs": {
                "by_mutations": {
                    "nested": {
                        "path": "mutations"
                    },
		    "aggs": {
			"inner": {
                            "filter": {
                                "bool": {
                                    "should": [
                                        {"match": {"mutations.mutation": i}}
                                for i in mutations
                                    ]
                                }
                            },
			    "aggs": {
				"by_name": {
				    "terms": {"field": "mutations.mutation"},
				    "aggs": {
				        "by_nested": {
				            "top_hits": {"size": 1}
				        }
				    }
				}
			    }
			}
		    }
		}
	    }
        }
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "by_mutations", "inner", "by_name", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = []
        for i in buckets:
            for j in i["by_nested"]["hits"]["hits"]:
                flattened_response.append(j["_source"])
        resp = {"success": True, "results": flattened_response}
        self.write(resp)
