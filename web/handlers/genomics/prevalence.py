from .util import transform_prevalence, transform_prevalence_by_location_and_tiime, compute_rolling_mean, create_nested_mutation_query, get_major_lineage_prevalence, compute_total_rolling_count, compute_rolling_mean_all_lineages
from .base import BaseHandler
from tornado import gen
import pandas as pd
from datetime import timedelta

class PrevalenceByLocationHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_division = self.get_argument("division", None)
        query_mutations = self.get_argument("mutations", None)
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        cumulative = self.get_argument("cumulative", None)
        cumulative = True if cumulative == "true" else False
        filter_term = {"country": query_country} if query_country is not None else {"division": query_division}
        query = {
            "size": 0,
            "aggs": {
                "prevalence": {
                    "filter" : {
                        "term" : filter_term
                    },
                    "aggs": {
                        "count": {
                            "terms": {
                                "field": "date_collected",
                                "size": self.size
                            },
                            "aggs": {
                                "lineage_count": {
                                    "filter": {}
                                }
                            }
                        }
                    }
                }
            }
        }
        query_obj = create_nested_mutation_query(division = query_division, country = query_country, lineage = query_pangolin_lineage, mutations = query_mutations)
        query["aggs"]["prevalence"]["aggs"]["count"]["aggs"]["lineage_count"]["filter"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "prevalence", "count", "buckets"]
        resp = transform_prevalence(resp, path_to_results, cumulative)
        self.write(resp)

# Most recent prevalence
class PrevalenceByLocationAndTimeHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_detected = self.get_argument("detected", None)
        query_mutations = self.get_argument("mutations", None)
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query_detected = True if query_detected == "true" else False
        query = {
            "size": 0,
            "aggs": {
                "sub_date_buckets": {
                    "composite": {
                        "size": 10000,
                        "sources": [
                            {"date_collected": { "terms": {"field": "date_collected"}}},
                            # {"country": { "terms": {"field": "country"} }}
                        ]
                    },
                    "aggregations": {
                        "lineage_count": {
                            "filter": {}
                        }
                    }
                }
            }
        }
        if query_division is not None:
            query["query"] = {
	        "term": {"division": query_division}
            }
            query["aggs"]["sub_date_buckets"]["composite"]["sources"].append(
                {"sub": { "terms": {"field": "location"} }}
            )
        elif query_country is not None:
            query["query"] = {
	        "term": {"country": query_country}
            }
            query["aggs"]["sub_date_buckets"]["composite"]["sources"].append(
                {"sub": { "terms": {"field": "division"} }}
            )
        else:
            query["aggs"]["sub_date_buckets"]["composite"]["sources"].append(
                {"sub": { "terms": {"field": "country"} }}
            )
        query_obj = create_nested_mutation_query(lineage = query_pangolin_lineage, mutations = query_mutations)
        query["aggs"]["sub_date_buckets"]["aggregations"]["lineage_count"]["filter"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        ctr = 0
        buckets = resp["aggregations"]["sub_date_buckets"]["buckets"]
        # Get all paginated results
        while "after_key" in resp["aggregations"]["sub_date_buckets"]:
            query["aggs"]["sub_date_buckets"]["composite"]["after"] = resp["aggregations"]["sub_date_buckets"]["after_key"]
            resp = yield self.asynchronous_fetch(query)
            buckets.extend(resp["aggregations"]["sub_date_buckets"]["buckets"])
        dict_response = {"success": True, "results": []}
        if len(buckets) > 0:
            flattened_response = [{
                "date": i["key"]["date_collected"],
                "name": i["key"]["sub"],
                "total_count": i["doc_count"],
                "lineage_count": i["lineage_count"]["doc_count"]
            } for i in buckets if len(i["key"]["date_collected"].split("-")) > 1 and "XX" not in i["key"]["date_collected"]]
            dict_response = transform_prevalence_by_location_and_tiime(flattened_response, query_detected)
        resp = {"success": True, "results": dict_response}
        self.write(resp)

# Get global prevalence of lineage by date
class PrevalenceHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_mutations = self.get_argument("mutations", None)
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
                            "filter": {}
                        }
                    }
                }
            }
        }
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query_obj = create_nested_mutation_query(lineage = query_pangolin_lineage, mutations = query_mutations)
        query["aggs"]["prevalence"]["aggs"]["lineage_count"]["filter"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "prevalence", "buckets"]
        resp = transform_prevalence(resp, path_to_results, cumulative)
        self.write(resp)

class PrevalenceAllLineagesByLocationHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query_other_threshold = self.get_argument("other_threshold", 0.05)
        query_other_threshold = float(query_other_threshold)
        query_nday_threshold = self.get_argument("nday_threshold", 10)
        query_nday_threshold = float(query_nday_threshold)
        query_other_exclude = self.get_argument("other_exclude", None)
        query_other_exclude = query_other_exclude.split(",") if query_other_exclude is not None else []
        query = {
            "size": 0,
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
        if query_division != None:
            query["query"] = {
                "term" : { "division" : query_division }
            }
        elif query_country != None:
            query["query"] = {
                "term" : { "country" : query_country }
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
        df_response = get_major_lineage_prevalence(df_response, "date", query_other_exclude, query_other_threshold, query_nday_threshold)
        df_response = df_response.groupby("lineage").apply(compute_rolling_mean_all_lineages, "date", "lineage_count", "lineage_count_rolling", "lineage")
        df_response = df_response.groupby("date").apply(compute_total_rolling_count, "lineage_count_rolling", "total_count_rolling")
        df_response.loc[:, "prevalence_rolling"] = df_response["lineage_count_rolling"]/df_response["total_count_rolling"]
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        resp = {"success": True, "results": df_response[["date", "total_count", "lineage_count", "lineage", "prevalence", "prevalence_rolling"]].to_dict(orient="records")}
        self.write(resp)

class PrevalenceByAAPositionHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_str = self.get_argument("name", None)
        query_country = self.get_argument("country", None)
        query_division = self.get_argument("division", None)
        query_gene = query_str.split(":")[0]
        query_aa_position = int(query_str.split(":")[1])
        # Get ref codon
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
                                    "must": [
                                        {"match": {"mutations.codon_num": query_aa_position}},
                                        {"match": {"mutations.gene": query_gene}}
                                    ]
                                }
                            },
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
        resp = yield self.asynchronous_fetch(query)
        tmp_ref = resp["aggregations"]["by_mutations"]["inner"]["by_nested"]["hits"]["hits"]
        dict_response = []
        if len(tmp_ref) > 0:
            ref_aa = tmp_ref[0]["_source"]["ref_aa"]
            query = {
	        "aggs": {
	            "by_date": {
		        "terms": {
                            "field": "date_collected",
                            "size": self.size
                        },
                        "aggs": {
                            "by_mutations": {
                                "nested": {
                                    "path": "mutations"
                                },
		                "aggs": {
			            "inner": {
                                        "filter": {
                                            "bool": {
                                                "must": [
                                                    {"match": {"mutations.codon_num": query_aa_position}},
                                                    {"match": {"mutations.gene": query_gene}}
                                                ]
                                            }
                                        },
			                "aggs": {
				            "by_name": {
				                "terms": {"field": "mutations.alt_aa"}
				            }
			                }
			            }
		                }
		            }
	                }
		    }
	        }
            }
            if query_division != None:
                query["query"]= {
                    "match": {
                        "country": query_division
                    }
                }
            elif query_country != None:
                query["query"]= {
                    "match": {
                        "country": query_country
                    }
                }
            resp = yield self.asynchronous_fetch(query)
            buckets = resp
            path_to_results = ["aggregations", "by_date", "buckets"]
            for i in path_to_results:
                buckets = buckets[i]
            flattened_response = []
            for d in buckets:
                alt_count = 0
                for m in d["by_mutations"]["inner"]["by_name"]["buckets"]:
                    if m["key"] == "None":
                        continue
                    flattened_response.append({
                        "date": d["key"],
                        "total_count": d["doc_count"],
                        "aa": m["key"],
                        "aa_count": m["doc_count"]
                    })
                    alt_count += m["doc_count"]
                flattened_response.append({
                    "date": d["key"],
                    "total_count": d["doc_count"],
                    "aa": ref_aa,
                    "aa_count": d["doc_count"] - alt_count
                })
            df_response = (
                pd.DataFrame(flattened_response)
                .assign(
                    date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"),
                    prevalence = lambda x: x["aa_count"]/x["total_count"]
                )
                .sort_values("date")
            )
            df_response = df_response.groupby("aa").apply(compute_rolling_mean, "date", "prevalence", "prevalence_rolling")
            df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
            dict_response = df_response.to_dict(orient="records")
        resp = {"success": True, "results": dict_response}
        self.write(resp)
