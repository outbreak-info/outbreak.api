from .util import transform_prevalence, transform_prevalence_by_location_and_tiime, compute_rolling_mean, create_nested_mutation_query, get_major_lineage_prevalence, compute_total_count, compute_rolling_mean_all_lineages, expand_dates, parse_location_id_to_query, create_iterator
from .base import BaseHandler
from tornado import gen
import pandas as pd
from datetime import timedelta, datetime as dt

# Get global prevalence of lineage by date
class GlobalPrevalenceByTimeHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
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
        query_pangolin_lineage = query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
        query_obj = create_nested_mutation_query(lineages = query_pangolin_lineage, mutations = query_mutations)
        query["aggs"]["prevalence"]["aggs"]["lineage_count"]["filter"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "prevalence", "buckets"]
        resp = transform_prevalence(resp, path_to_results, cumulative)
        return {
            "success": True,
            "results": resp
        }

class PrevalenceByLocationAndTimeHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
        query_location = self.get_argument("location_id", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_pangolin_lineage = query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
        query_mutations = self.get_argument("mutations", None)
        query_mutations = query_mutations.split(" AND ") if query_mutations is not None else []
        cumulative = self.get_argument("cumulative", None)
        cumulative = True if cumulative == "true" else False
        results = {}
        for i,j in create_iterator(query_pangolin_lineage, query_mutations):
            query = {
                "size": 0,
                "aggs": {
                    "prevalence": {
                        "filter": {
                            "bool": {
                                "must": []
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
                                        "filter": {}
                                    }
                                }
                            }
                        }
                    }
                }
            }
            parse_location_id_to_query(query_location, query["aggs"]["prevalence"]["filter"])
            lineages = i.split(" OR ") if i is not None else []
            query_obj = create_nested_mutation_query(lineages = lineages, mutations = j, location_id = query_location)
            #print(query_obj)
            query["aggs"]["prevalence"]["aggs"]["count"]["aggs"]["lineage_count"]["filter"] = query_obj
            resp = yield self.asynchronous_fetch(query)
            path_to_results = ["aggregations", "prevalence", "count", "buckets"]
            resp = transform_prevalence(resp, path_to_results, cumulative)
            res_key = None
            if len(query_pangolin_lineage) > 0:
                res_key = " OR ".join(lineages)
            if len(query_mutations) > 0:
                res_key = "({}) AND ({})".format(res_key, " AND ".join(query_mutations)) if res_key is not None else " AND ".join(query_mutations)
            results[res_key] = resp
        return {
            "success": True,
            "results": results
        }

class CumulativePrevalenceByLocationHandler(BaseHandler):

    country_iso3_to_iso2 = {"BGD": "BD", "BEL": "BE", "BFA": "BF", "BGR": "BG", "BIH": "BA", "BRB": "BB", "WLF": "WF", "BLM": "BL", "BMU": "BM", "BRN": "BN", "BOL": "BO", "BHR": "BH", "BDI": "BI", "BEN": "BJ", "BTN": "BT", "JAM": "JM", "BVT": "BV", "BWA": "BW", "WSM": "WS", "BES": "BQ", "BRA": "BR", "BHS": "BS", "JEY": "JE", "BLR": "BY", "BLZ": "BZ", "RUS": "RU", "RWA": "RW", "SRB": "RS", "TLS": "TL", "REU": "RE", "TKM": "TM", "TJK": "TJ", "ROU": "RO", "TKL": "TK", "GNB": "GW", "GUM": "GU", "GTM": "GT", "SGS": "GS", "GRC": "GR", "GNQ": "GQ", "GLP": "GP", "JPN": "JP", "GUY": "GY", "GGY": "GG", "GUF": "GF", "GEO": "GE", "GRD": "GD", "GBR": "GB", "GAB": "GA", "SLV": "SV", "GIN": "GN", "GMB": "GM", "GRL": "GL", "GIB": "GI", "GHA": "GH", "OMN": "OM", "TUN": "TN", "JOR": "JO", "HRV": "HR", "HTI": "HT", "HUN": "HU", "HKG": "HK", "HND": "HN", "HMD": "HM", "VEN": "VE", "PRI": "PR", "PSE": "PS", "PLW": "PW", "PRT": "PT", "SJM": "SJ", "PRY": "PY", "IRQ": "IQ", "PAN": "PA", "PYF": "PF", "PNG": "PG", "PER": "PE", "PAK": "PK", "PHL": "PH", "PCN": "PN", "POL": "PL", "SPM": "PM", "ZMB": "ZM", "ESH": "EH", "EST": "EE", "EGY": "EG", "ZAF": "ZA", "ECU": "EC", "ITA": "IT", "VNM": "VN", "SLB": "SB", "ETH": "ET", "SOM": "SO", "ZWE": "ZW", "SAU": "SA", "ESP": "ES", "ERI": "ER", "MNE": "ME", "MDA": "MD", "MDG": "MG", "MAF": "MF", "MAR": "MA", "MCO": "MC", "UZB": "UZ", "MMR": "MM", "MLI": "ML", "MAC": "MO", "MNG": "MN", "MHL": "MH", "MKD": "MK", "MUS": "MU", "MLT": "MT", "MWI": "MW", "MDV": "MV", "MTQ": "MQ", "MNP": "MP", "MSR": "MS", "MRT": "MR", "IMN": "IM", "UGA": "UG", "TZA": "TZ", "MYS": "MY", "MEX": "MX", "ISR": "IL", "FRA": "FR", "IOT": "IO", "SHN": "SH", "FIN": "FI", "FJI": "FJ", "FLK": "FK", "FSM": "FM", "FRO": "FO", "NIC": "NI", "NLD": "NL", "NOR": "NO", "NAM": "NA", "VUT": "VU", "NCL": "NC", "NER": "NE", "NFK": "NF", "NGA": "NG", "NZL": "NZ", "NPL": "NP", "NRU": "NR", "NIU": "NU", "COK": "CK", "XKX": "XK", "CIV": "CI", "CHE": "CH", "COL": "CO", "CHN": "CN", "CMR": "CM", "CHL": "CL", "CCK": "CC", "CAN": "CA", "COG": "CG", "CAF": "CF", "COD": "CD", "CZE": "CZ", "CYP": "CY", "CXR": "CX", "CRI": "CR", "CUW": "CW", "CPV": "CV", "CUB": "CU", "SWZ": "SZ", "SYR": "SY", "SXM": "SX", "KGZ": "KG", "KEN": "KE", "SSD": "SS", "SUR": "SR", "KIR": "KI", "KHM": "KH", "KNA": "KN", "COM": "KM", "STP": "ST", "SVK": "SK", "KOR": "KR", "SVN": "SI", "PRK": "KP", "KWT": "KW", "SEN": "SN", "SMR": "SM", "SLE": "SL", "SYC": "SC", "KAZ": "KZ", "CYM": "KY", "SGP": "SG", "SWE": "SE", "SDN": "SD", "DOM": "DO", "DMA": "DM", "DJI": "DJ", "DNK": "DK", "VGB": "VG", "DEU": "DE", "YEM": "YE", "DZA": "DZ", "USA": "US", "URY": "UY", "MYT": "YT", "UMI": "UM", "LBN": "LB", "LCA": "LC", "LAO": "LA", "TUV": "TV", "TWN": "TW", "TTO": "TT", "TUR": "TR", "LKA": "LK", "LIE": "LI", "LVA": "LV", "TON": "TO", "LTU": "LT", "LUX": "LU", "LBR": "LR", "LSO": "LS", "THA": "TH", "ATF": "TF", "TGO": "TG", "TCD": "TD", "TCA": "TC", "LBY": "LY", "VAT": "VA", "VCT": "VC", "ARE": "AE", "AND": "AD", "ATG": "AG", "AFG": "AF", "AIA": "AI", "VIR": "VI", "ISL": "IS", "IRN": "IR", "ARM": "AM", "ALB": "AL", "AGO": "AO", "ATA": "AQ", "ASM": "AS", "ARG": "AR", "AUS": "AU", "AUT": "AT", "ABW": "AW", "IND": "IN", "ALA": "AX", "AZE": "AZ", "IRL": "IE", "IDN": "ID", "UKR": "UA", "QAT": "QA", "MOZ": "MZ"} # TODO: Move to separate class.

    @gen.coroutine
    def _get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_pangolin_lineage = query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
        query_detected = self.get_argument("detected", None)
        query_mutations = self.get_argument("mutations", None)
        query_location = self.get_argument("location_id", None)
        query_mutations = query_mutations.split(" AND ") if query_mutations is not None else []
        query_detected = True if query_detected == "true" else False
        query_ndays = self.get_argument("ndays", None)
        query_ndays = int(query_ndays) if query_ndays is not None else None
        results = {}
        for query_lineage, query_mutation in create_iterator(query_pangolin_lineage, query_mutations):
            query = {
                "size": 0,
                "aggs": {
                    "sub_date_buckets": {
                        "composite": {
                            "size": 10000,
                            "sources": [
                                {"date_collected": { "terms": {"field": "date_collected"}}}
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
            if query_location is not None: # Global
                query["query"] = parse_location_id_to_query(query_location)
            admin_level = 0
            if query_location is None:
                query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend([
                    {"sub": { "terms": {"field": "country"} }},
                    {"sub_id": { "terms": {"field": "country_id"} }}
                ])
                admin_level = 0
            elif len(query_location.split("_")) == 2:
                query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend([
                    {"sub_id": { "terms": {"field": "location_id"} }},
                    {"sub": { "terms": {"field": "location"} }}
                ])
                admin_level = 2
            elif len(query_location.split("_")) == 1:
                query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend([
                    {"sub_id": { "terms": {"field": "division_id"} }},
                    {"sub": { "terms": {"field": "division"} }}
                ])
                admin_level = 1
            query_lineages = query_lineage.split(" OR ") if query_lineage is not None else []
            query_obj = create_nested_mutation_query(lineages = query_lineages, mutations = query_mutation)
            query["aggs"]["sub_date_buckets"]["aggregations"]["lineage_count"]["filter"] = query_obj
            resp = yield self.asynchronous_fetch(query)
            ctr = 0
            buckets = resp["aggregations"]["sub_date_buckets"]["buckets"]
            # Get all paginated results
            while "after_key" in resp["aggregations"]["sub_date_buckets"]:
                query["aggs"]["sub_date_buckets"]["composite"]["after"] = resp["aggregations"]["sub_date_buckets"]["after_key"]
                resp = yield self.asynchronous_fetch(query)
                buckets.extend(resp["aggregations"]["sub_date_buckets"]["buckets"])
            dict_response = {}
            if len(buckets) > 0:
                flattened_response = []
                for i in buckets:
                    if len(i["key"]["date_collected"].split("-")) < 3 or "XX" in i["key"]["date_collected"]:
                        continue
                    # Check for None and out of state
                    if i["key"]["sub"].lower().replace("-", "").replace(" ", "") == "outofstate":
                        i["key"]["sub"] = "Out of state"
                    if i["key"]["sub"].lower() in ["none", "unknown"]:
                        i["key"]["sub"] = "Unknown"
                    rec = {
                        "date": i["key"]["date_collected"],
                        "name": i["key"]["sub"],
                        "id": i["key"]["sub_id"],
                        "total_count": i["doc_count"],
                        "lineage_count": i["lineage_count"]["doc_count"]
                    }
                    if admin_level == 1:
                        rec["id"] = "_".join([query_location, self.country_iso3_to_iso2[query_location]+"-"+i["key"]["sub_id"] if query_location in self.country_iso3_to_iso2 else query_location + "-" + i["key"]["sub_id"]])
                    elif admin_level == 2:
                        rec["id"] = "_".join([query_location, i["key"]["sub_id"]])
                    flattened_response.append(rec)
                dict_response = transform_prevalence_by_location_and_tiime(flattened_response, query_ndays, query_detected)
            res_key = None
            if query_lineage is not None: # create_iterator will never return empty list for lineages
                res_key = " OR ".join(query_lineages)
            if len(query_mutations) > 0:
                res_key = "({}) AND ({})".format(res_key, " AND ".join(query_mutations)) if res_key is not None else " AND ".join(query_mutations)
            results[res_key] = dict_response
        return {
            "success": True,
            "results": results
        }

class PrevalenceAllLineagesByLocationHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
        query_location = self.get_argument("location_id", None)
        query_window = self.get_argument("window", None)
        query_window = int(query_window) if query_window is not None else None
        query_other_threshold = self.get_argument("other_threshold", 0.05)
        query_other_threshold = float(query_other_threshold)
        query_nday_threshold = self.get_argument("nday_threshold", 10)
        query_nday_threshold = float(query_nday_threshold)
        query_ndays = self.get_argument("ndays", 180)
        query_ndays = int(query_ndays)
        query_other_exclude = self.get_argument("other_exclude", None)
        query_other_exclude = query_other_exclude.split(",") if query_other_exclude is not None else []
        query_cumulative = self.get_argument("cumulative", None)
        query_cumulative = True if query_cumulative == "true" else False
        query = {
            "size": 0,
            "query": {},
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
        query["query"] = parse_location_id_to_query(query_location)
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
        if query_window is not None:
            df_response = df_response[df_response["date"] >= (dt.now() - timedelta(days = query_window))]
        df_response = get_major_lineage_prevalence(df_response, "date", query_other_exclude, query_other_threshold, query_nday_threshold, query_ndays)
        if not query_cumulative:
            df_response = df_response.groupby("lineage").apply(compute_rolling_mean_all_lineages, "date", "lineage_count", "lineage_count_rolling", "lineage").reset_index()
            df_response = df_response.groupby("date").apply(compute_total_count, "lineage_count_rolling", "total_count_rolling")
            df_response.loc[:, "prevalence_rolling"] = df_response["lineage_count_rolling"]/df_response["total_count_rolling"]
            df_response.loc[df_response["prevalence_rolling"].isna(), "prevalence_rolling"] = 0 # Prevalence is 0 if total_count_rolling == 0.
            df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
            df_response = df_response.fillna("None")
            df_response = df_response[["date", "total_count", "lineage_count", "lineage", "prevalence", "prevalence_rolling"]]
        else:
            df_response = df_response.groupby("lineage").apply(expand_dates, df_response["date"].min(), df_response["date"].max(), "date", "lineage").reset_index()
            df_response = df_response.groupby("date").apply(compute_total_count, "lineage_count", "total_count").reset_index()
            df_response = df_response.groupby("lineage").agg({"total_count": "sum", "lineage_count": "sum"}).reset_index()
            df_response.loc[:,"prevalence"] = df_response["lineage_count"]/df_response["total_count"]
        resp = {"success": True, "results": df_response.to_dict(orient="records")}
        return resp

class PrevalenceByAAPositionHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
        query_str = self.get_argument("name", None)
        query_location = self.get_argument("location", None)
        query_lineage = self.get_argument("pangolin_lineage", None)
        # query_country = self.get_argument("country", None)
        # query_division = self.get_argument("division", None)
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
            if query_location is not None:
                query["query"] = parse_location_id_to_query(query_location, query["aggs"]["prevalence"]["filter"])
            if query_lineage is not None:
                if "query" in query:
                    query["query"]["bool"]["must"].append({
                        "term": {
                            "pangolin_lineage": query_lineage
                        }
                    })
                else:
                    query["query"] = {
                        "term": {
                            "pangolin_lineage": query_lineage
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
        return resp


