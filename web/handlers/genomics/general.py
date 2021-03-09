import pandas as pd
from .base import BaseHandler
from tornado import gen
from .util import create_nested_mutation_query, parse_location_id_to_query

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

class LocationDetailsHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query_str = self.get_argument("id", None)
        query_ids = query_str.split("_")
        query = {
            "query": {},
            "aggs": {
                "country": {
                    "terms": {
                        "field": "country"
                    }
                }
            }
        }
        if len(query_ids) >= 2:
            query["aggs"]["country"]["aggs"] = {
                "division": {
                    "terms": {
                        "field": "division"
                    }
                }
            }
        if len(query_ids) == 3: # 3 is max length
            query["aggs"]["country"]["aggs"]["division"]["aggs"] = {
                "location": {
                    "terms": {
                        "field": "location"
                    }
                }
            }
        query["query"] = parse_location_id_to_query(query_str)
        resp = yield self.asynchronous_fetch(query)
        # resp = {"success": True, "results": flattened_response}
        self.write(resp)


class LocationHandler(BaseHandler):

    # Use dict to map to NE IDs from epi data
    country_iso3_to_iso2 = {"BGD": "BD", "BEL": "BE", "BFA": "BF", "BGR": "BG", "BIH": "BA", "BRB": "BB", "WLF": "WF", "BLM": "BL", "BMU": "BM", "BRN": "BN", "BOL": "BO", "BHR": "BH", "BDI": "BI", "BEN": "BJ", "BTN": "BT", "JAM": "JM", "BVT": "BV", "BWA": "BW", "WSM": "WS", "BES": "BQ", "BRA": "BR", "BHS": "BS", "JEY": "JE", "BLR": "BY", "BLZ": "BZ", "RUS": "RU", "RWA": "RW", "SRB": "RS", "TLS": "TL", "REU": "RE", "TKM": "TM", "TJK": "TJ", "ROU": "RO", "TKL": "TK", "GNB": "GW", "GUM": "GU", "GTM": "GT", "SGS": "GS", "GRC": "GR", "GNQ": "GQ", "GLP": "GP", "JPN": "JP", "GUY": "GY", "GGY": "GG", "GUF": "GF", "GEO": "GE", "GRD": "GD", "GBR": "GB", "GAB": "GA", "SLV": "SV", "GIN": "GN", "GMB": "GM", "GRL": "GL", "GIB": "GI", "GHA": "GH", "OMN": "OM", "TUN": "TN", "JOR": "JO", "HRV": "HR", "HTI": "HT", "HUN": "HU", "HKG": "HK", "HND": "HN", "HMD": "HM", "VEN": "VE", "PRI": "PR", "PSE": "PS", "PLW": "PW", "PRT": "PT", "SJM": "SJ", "PRY": "PY", "IRQ": "IQ", "PAN": "PA", "PYF": "PF", "PNG": "PG", "PER": "PE", "PAK": "PK", "PHL": "PH", "PCN": "PN", "POL": "PL", "SPM": "PM", "ZMB": "ZM", "ESH": "EH", "EST": "EE", "EGY": "EG", "ZAF": "ZA", "ECU": "EC", "ITA": "IT", "VNM": "VN", "SLB": "SB", "ETH": "ET", "SOM": "SO", "ZWE": "ZW", "SAU": "SA", "ESP": "ES", "ERI": "ER", "MNE": "ME", "MDA": "MD", "MDG": "MG", "MAF": "MF", "MAR": "MA", "MCO": "MC", "UZB": "UZ", "MMR": "MM", "MLI": "ML", "MAC": "MO", "MNG": "MN", "MHL": "MH", "MKD": "MK", "MUS": "MU", "MLT": "MT", "MWI": "MW", "MDV": "MV", "MTQ": "MQ", "MNP": "MP", "MSR": "MS", "MRT": "MR", "IMN": "IM", "UGA": "UG", "TZA": "TZ", "MYS": "MY", "MEX": "MX", "ISR": "IL", "FRA": "FR", "IOT": "IO", "SHN": "SH", "FIN": "FI", "FJI": "FJ", "FLK": "FK", "FSM": "FM", "FRO": "FO", "NIC": "NI", "NLD": "NL", "NOR": "NO", "NAM": "NA", "VUT": "VU", "NCL": "NC", "NER": "NE", "NFK": "NF", "NGA": "NG", "NZL": "NZ", "NPL": "NP", "NRU": "NR", "NIU": "NU", "COK": "CK", "XKX": "XK", "CIV": "CI", "CHE": "CH", "COL": "CO", "CHN": "CN", "CMR": "CM", "CHL": "CL", "CCK": "CC", "CAN": "CA", "COG": "CG", "CAF": "CF", "COD": "CD", "CZE": "CZ", "CYP": "CY", "CXR": "CX", "CRI": "CR", "CUW": "CW", "CPV": "CV", "CUB": "CU", "SWZ": "SZ", "SYR": "SY", "SXM": "SX", "KGZ": "KG", "KEN": "KE", "SSD": "SS", "SUR": "SR", "KIR": "KI", "KHM": "KH", "KNA": "KN", "COM": "KM", "STP": "ST", "SVK": "SK", "KOR": "KR", "SVN": "SI", "PRK": "KP", "KWT": "KW", "SEN": "SN", "SMR": "SM", "SLE": "SL", "SYC": "SC", "KAZ": "KZ", "CYM": "KY", "SGP": "SG", "SWE": "SE", "SDN": "SD", "DOM": "DO", "DMA": "DM", "DJI": "DJ", "DNK": "DK", "VGB": "VG", "DEU": "DE", "YEM": "YE", "DZA": "DZ", "USA": "US", "URY": "UY", "MYT": "YT", "UMI": "UM", "LBN": "LB", "LCA": "LC", "LAO": "LA", "TUV": "TV", "TWN": "TW", "TTO": "TT", "TUR": "TR", "LKA": "LK", "LIE": "LI", "LVA": "LV", "TON": "TO", "LTU": "LT", "LUX": "LU", "LBR": "LR", "LSO": "LS", "THA": "TH", "ATF": "TF", "TGO": "TG", "TCD": "TD", "TCA": "TC", "LBY": "LY", "VAT": "VA", "VCT": "VC", "ARE": "AE", "AND": "AD", "ATG": "AG", "AFG": "AF", "AIA": "AI", "VIR": "VI", "ISL": "IS", "IRN": "IR", "ARM": "AM", "ALB": "AL", "AGO": "AO", "ATA": "AQ", "ASM": "AS", "ARG": "AR", "AUS": "AU", "AUT": "AT", "ABW": "AW", "IND": "IN", "ALA": "AX", "AZE": "AZ", "IRL": "IE", "IDN": "ID", "UKR": "UA", "QAT": "QA", "MOZ": "MZ"}

    @gen.coroutine
    def get(self):
        query_str = self.get_argument("name", None)
        query = {
            "size": 0,
            "aggs": {
                "country_agg": {
                    "filter": {
                        "wildcard": {
                            "country_lower": {
                                "value": query_str
                            }
                        }
                    },
                    "aggs": {
                        "country_sub_agg": {
                            "terms": {
                                "field": "country"
                            },
                            "aggs": {
                                "country_id": {
                                    "terms": {
                                        "field": "country_id"
                                    }
                                }
                            }
                        }
                    }
                },
                "division_agg": {
                    "filter": {
                        "wildcard": {
                            "division_lower": {
                                "value": query_str
                            }
                        }
                    },
                    "aggs": {
                        "division_sub_agg": {
                            "terms": {
                                "field": "division"
                            },
                            "aggs": {
                                "country": {
                                    "terms": {
                                        "field": "country"
                                    },
                                    "aggs": {
                                        "country_id": {
                                            "terms": {
                                                "field": "country_id"
                                            },
                                            "aggs": {
                                                "division_id": {
                                                    "terms": {
                                                        "field": "division_id"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "location_agg": {
                    "filter": {
                        "wildcard": {
                            "location_lower": {
                                "value": query_str
                            }
                        }
                    },
                    "aggs": {
                        "location_sub_agg": {
                            "terms": {
                                "field": "location"
                            },
                            "aggs": {
                                "country": {
                                    "terms": {
                                        "field": "country"
                                    },
                                    "aggs": {
                                        "country_id": {
                                            "terms": {
                                                "field": "country_id"
                                            },
                                            "aggs": {
                                                "division": {
                                                    "terms": {
                                                        "field": "division"
                                                    },
                                                    "aggs": {
                                                        "division_id": {
                                                            "terms": {
                                                                "field": "division_id"
                                                            },
                                                            "aggs": {
                                                                "location_id": {
                                                                    "terms": {
                                                                        "field": "location_id"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
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
        # Parse countries
        flattened_response = []
        for rec in resp["aggregations"]["country_agg"]["country_sub_agg"]["buckets"]:
            for rec_id in rec["country_id"]["buckets"][:1]:
                flattened_response.append({
                    "country": rec["key"],
                    "country_id": rec_id["key"], # There should be only 1 ID associated with each country. Used this in lieu of composite aggregations. Composite aggregations don't work as a child aggregation.
                    "total_count": rec_id["doc_count"] # Should be same as rec["doc_count"] siince only 1 ID per location
                })
        # Parse divisions
        for rec in resp["aggregations"]["division_agg"]["division_sub_agg"]["buckets"]:
            for rec_country in rec["country"]["buckets"]: # Multiple countries per division name
                for rec_country_id in rec_country["country_id"]["buckets"][:1]: # There should be only 1 ID associated with each country. Used this in lieu of composite aggregations. Composite aggregations don't work as a child aggregation.
                    for rec_division_id in rec_country_id["division_id"]["buckets"][:1]: # There should be only 1 ID associated with each division within a country. Used this in lieu of composite aggregations. Composite aggregations don't work as a child aggregation.
                        flattened_response.append({
                            "division": rec["key"],
                            "division_id": rec_division_id["key"],
                            "country": rec_country["key"],
                            "country_id": rec_country_id["key"], # There should be only 1 ID associated with each country. Used this in lieu of composite aggregations. Composite aggregations don't work as a child aggregation.
                            "total_count": rec_division_id["doc_count"] # Should be same as rec_country["doc_count"] siince only 1 ID per division
                        })
        # Parse counties
        for rec in resp["aggregations"]["location_agg"]["location_sub_agg"]["buckets"]:
            for rec_country in rec["country"]["buckets"]: # Multiple countries per county
                for rec_country_id in rec_country["country_id"]["buckets"][:1]: # There should be only 1 ID associated with each country. Used this in lieu of composite aggregations. Composite aggregations don't work as a child aggregation.
                    for rec_division in rec_country_id["division"]["buckets"]: # Multiple divisions per county
                        for rec_division_id in rec_division["division_id"]["buckets"][:1]: # There should be only 1 ID associated with each division within a country. Used this in lieu of composite aggregations. Composite aggregations don't work as a child aggregation.
                            for rec_location_id in rec_division_id["location_id"]["buckets"][:1]: # 1 location id per division
                                flattened_response.append({
                                    "location": rec["key"],
                                    "location_id": rec_location_id["key"],
                                    "division": rec_division["key"],
                                    "division_id": rec_division_id["key"],
                                    "country": rec_country["key"],
                                    "country_id": rec_country_id["key"], # There should be only 1 ID associated with each country. Used this in lieu of composite aggregations. Composite aggregations don't work as a child aggregation.
                                    "total_count": rec_location_id["doc_count"] # Should be same as rec_country["doc_count"] siince only 1 ID per division
                                })
        # Add full names and location ids
        for rec in flattened_response:
            _name = ""
            _id = ""
            admin_level = 0
            if "location_id" in rec:
                _name = ", ".join([rec["location"], rec["division"], rec["country"]])
                _id = "_".join([rec["country_id"], self.country_iso3_to_iso2[rec["country_id"]] + "-" + rec["division_id"], rec["location_id"]]) # ID in the format
                admin_level = 2
            elif "division_id" in rec:
                _name = ", ".join([rec["division"], rec["country"]])
                _id = "_".join([rec["country_id"], self.country_iso3_to_iso2[rec["country_id"]] + "-" + rec["division_id"]]) # ID in the format
                admin_level = 1
            else:
                _name = rec["country"]
                _id = rec["country_id"]
            rec["label"] = _name
            rec["id"] = _id
            rec["admin_level"] = admin_level
        resp = {"success": True, "results": flattened_response}
        self.write(resp)

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
