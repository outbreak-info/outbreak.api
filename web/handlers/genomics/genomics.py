from tornado     import gen

from biothings.web.handlers import BaseHandler as BiothingsBaseHandler


# Count total number of sequences of lineage by country
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

# Calculate total number of sequences with a particular lineage at Country
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
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "prevalence", "count", "buckets"]
        resp = transform_prevalence(resp, path_to_results)
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
                                "term" : { "pangolin_lineage" : query_pangolin_lineage },
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
            "country": i["key"]["country"],
            "total_count": i["doc_count"],
            "lineage_count": i["lineage_count"]["doc_count"]
        } for i in buckets if len(i["key"]["date_collected"].split("-")) > 1 and "XX" not in i["key"]["date_collected"]]
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
            .sort_values("date")
        )
        grps = []
        for ctr,(n,grp) in enumerate(df_response.groupby("country")):
            grp = grp.sort_values("date")
            first_date = grp["date"][grp["lineage_count"] > 0].min()
            grp = grp[grp["date"] >= first_date]
            grp.loc[:, "cum_total_count"] = grp["total_count"].cumsum()
            grp.loc[:, "cum_lineage_count"] = grp["lineage_count"].cumsum()
            grps.append(grp.tail(1))
        df_response = pd.concat(grps)
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        d = calculate_proportion(df_response["cum_lineage_count"], df_response["cum_total_count"])
        df_response.loc[:, "proportion"] = d[0]
        df_response.loc[:, "proportion_ci_lower"] = d[1]
        df_response.loc[:, "proportion_ci_upper"] = d[2]
        dict_response = df_response.to_dict(orient="records")
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
        print(len(buckets))
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

# Most recent collection date per lineage
class MostRecentCollectionDate(BaseHandler):

    @gen.coroutine
    def get(self):
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
                    "lineage": i["key"]
                })
        print(flattened_response[0])
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
            .sort_values("date")
        )
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df_response = df_response.groupby(["lineage"]).nth(-1)
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
        pangolin_lineage = self.get_argument("lineage", None)
        frequency = self.get_argument("frequency", None)
        frequency = float(frequency) if frequency != None else 0.8
        query =  {
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
		        "mutations_inset": {
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
        path_to_results = ["aggregations", "mutations", "mutations_inset", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{
            "name": i["key"],
            "mutation_count": i["doc_count"],
            "lineage_count": resp["hits"]["total"]
        } for i in buckets]
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(
                gene = lambda x: x["name"].apply(lambda k: k.split(":")[0]),
                ref_aa = lambda x: x["name"].apply(lambda k: re.findall("[A-Z]+", k.split(":")[1])[0] if "DEL" not in k and "_" not in k else k),
                alt_aa = lambda x: x["name"].apply(lambda k: re.findall("[A-Z]+", k.split(":")[1])[1] if "DEL" not in k and "_" not in k else k.split(":")[1]),
                codon_num = lambda x: x["name"].apply(lambda k: re.findall("[0-9]+", k.split(":")[1])[0] if "DEL" not in k and "_" not in k else k.split(":")[1])
            )
        )
        df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
        df_response.loc[:, "prevalence"] = df_response["mutation_count"]/df_response["lineage_count"]
        df_response = df_response[df_response["prevalence"] >= frequency]
        resp = {"success": True, "results": df_response.to_dict(orient="records")}
        self.write(resp)
