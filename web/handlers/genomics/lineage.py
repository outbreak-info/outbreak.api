from .base import BaseHandler
from tornado import gen
import pandas as pd
from .util import create_nested_mutation_query, calculate_proportion

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

    gene_mapping = {
        "orf1a" : "ORF1a",
        "orf1b" : "ORF1b",
        "s" : "S",
        "orf3a" : "ORF3a",
        "e": "E",
        "m" : "M",
        "orf6": "ORF6",
        "orf7a" : "ORF7a",
        "orf7b" : "ORF7b",
        "orf8" : "ORF8",
        "n" : "N",
        "orf10" : "ORF10"
    }

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
                    gene = lambda x: x["mutation"].apply(lambda k: self.gene_mapping[k.split(":")[0]] if k.split(":")[0] in self.gene_mapping else k.split(":")[0]),
                    ref_aa = lambda x: x["mutation"].apply(lambda k: re.findall("[A-Za-z]+", k.split(":")[1])[0] if "DEL" not in k and "del" not in k and "_" not in k else k).str.upper(),
                    alt_aa = lambda x: x["mutation"].apply(lambda k: re.findall("[A-Za-z]+", k.split(":")[1])[1] if "DEL" not in k and "del" not in k and "_" not in k else k.split(":")[1]).str.upper(),
                    codon_num = lambda x: x["mutation"].apply(lambda k: int(re.findall("[0-9]+", k.split(":")[1])[0])),
                    type = lambda x: x["mutation"].apply(lambda k: "deletion" if "DEL" in k or "del" in k else "substitution")
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

class MutationsByLineage(BaseHandler):
    @gen.coroutine
    def get(self):
        query_mutations = self.get_argument("mutations", None)
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query = {
            "size": 0,
            "aggs": {
	        "lineage": {
                    "terms": {"field": "pangolin_lineage", "size": self.size},
                    "aggs": {
                        "mutations": {
                            "filter": {}
			}
                    }
                }
            }
        }
        query["aggs"]["lineage"]["aggs"]["mutations"]["filter"] = create_nested_mutation_query(mutations = query_mutations)
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "lineage", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = []
        for i in buckets:
            if not i["mutations"]["doc_count"] > 0 or i["key"] == "none":
                continue
            flattened_response.append({
                "pangolin_lineage": i["key"],
                "lineage_count": i["doc_count"],
                "mutation_count": i["mutations"]["doc_count"]
            })
        df_response = pd.DataFrame(flattened_response)
        prop = calculate_proportion(df_response["mutation_count"], df_response["lineage_count"])
        df_response.loc[:, "proportion"] = prop[0]
        df_response.loc[:, "proportion_ci_lower"] = prop[1]
        df_response.loc[:, "proportion_ci_upper"] = prop[2]
        resp = {"success": True, "results": df_response.to_dict(orient="records")}
        self.write(resp)
