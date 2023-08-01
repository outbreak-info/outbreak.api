import pandas as pd
from .base import BaseHandler
from tornado import gen
from .util import create_nested_mutation_query, parse_location_id_to_query, get_total_hits

class SequenceCountHandler(BaseHandler):

    country_iso3_to_iso2 = {"BGD": "BD", "BEL": "BE", "BFA": "BF", "BGR": "BG", "BIH": "BA", "BRB": "BB", "WLF": "WF", "BLM": "BL", "BMU": "BM", "BRN": "BN", "BOL": "BO", "BHR": "BH", "BDI": "BI", "BEN": "BJ", "BTN": "BT", "JAM": "JM", "BVT": "BV", "BWA": "BW", "WSM": "WS", "BES": "BQ", "BRA": "BR", "BHS": "BS", "JEY": "JE", "BLR": "BY", "BLZ": "BZ", "RUS": "RU", "RWA": "RW", "SRB": "RS", "TLS": "TL", "REU": "RE", "TKM": "TM", "TJK": "TJ", "ROU": "RO", "TKL": "TK", "GNB": "GW", "GUM": "GU", "GTM": "GT", "SGS": "GS", "GRC": "GR", "GNQ": "GQ", "GLP": "GP", "JPN": "JP", "GUY": "GY", "GGY": "GG", "GUF": "GF", "GEO": "GE", "GRD": "GD", "GBR": "GB", "GAB": "GA", "SLV": "SV", "GIN": "GN", "GMB": "GM", "GRL": "GL", "GIB": "GI", "GHA": "GH", "OMN": "OM", "TUN": "TN", "JOR": "JO", "HRV": "HR", "HTI": "HT", "HUN": "HU", "HKG": "HK", "HND": "HN", "HMD": "HM", "VEN": "VE", "PRI": "PR", "PSE": "PS", "PLW": "PW", "PRT": "PT", "SJM": "SJ", "PRY": "PY", "IRQ": "IQ", "PAN": "PA", "PYF": "PF", "PNG": "PG", "PER": "PE", "PAK": "PK", "PHL": "PH", "PCN": "PN", "POL": "PL", "SPM": "PM", "ZMB": "ZM", "ESH": "EH", "EST": "EE", "EGY": "EG", "ZAF": "ZA", "ECU": "EC", "ITA": "IT", "VNM": "VN", "SLB": "SB", "ETH": "ET", "SOM": "SO", "ZWE": "ZW", "SAU": "SA", "ESP": "ES", "ERI": "ER", "MNE": "ME", "MDA": "MD", "MDG": "MG", "MAF": "MF", "MAR": "MA", "MCO": "MC", "UZB": "UZ", "MMR": "MM", "MLI": "ML", "MAC": "MO", "MNG": "MN", "MHL": "MH", "MKD": "MK", "MUS": "MU", "MLT": "MT", "MWI": "MW", "MDV": "MV", "MTQ": "MQ", "MNP": "MP", "MSR": "MS", "MRT": "MR", "IMN": "IM", "UGA": "UG", "TZA": "TZ", "MYS": "MY", "MEX": "MX", "ISR": "IL", "FRA": "FR", "IOT": "IO", "SHN": "SH", "FIN": "FI", "FJI": "FJ", "FLK": "FK", "FSM": "FM", "FRO": "FO", "NIC": "NI", "NLD": "NL", "NOR": "NO", "NAM": "NA", "VUT": "VU", "NCL": "NC", "NER": "NE", "NFK": "NF", "NGA": "NG", "NZL": "NZ", "NPL": "NP", "NRU": "NR", "NIU": "NU", "COK": "CK", "XKX": "XK", "CIV": "CI", "CHE": "CH", "COL": "CO", "CHN": "CN", "CMR": "CM", "CHL": "CL", "CCK": "CC", "CAN": "CA", "COG": "CG", "CAF": "CF", "COD": "CD", "CZE": "CZ", "CYP": "CY", "CXR": "CX", "CRI": "CR", "CUW": "CW", "CPV": "CV", "CUB": "CU", "SWZ": "SZ", "SYR": "SY", "SXM": "SX", "KGZ": "KG", "KEN": "KE", "SSD": "SS", "SUR": "SR", "KIR": "KI", "KHM": "KH", "KNA": "KN", "COM": "KM", "STP": "ST", "SVK": "SK", "KOR": "KR", "SVN": "SI", "PRK": "KP", "KWT": "KW", "SEN": "SN", "SMR": "SM", "SLE": "SL", "SYC": "SC", "KAZ": "KZ", "CYM": "KY", "SGP": "SG", "SWE": "SE", "SDN": "SD", "DOM": "DO", "DMA": "DM", "DJI": "DJ", "DNK": "DK", "VGB": "VG", "DEU": "DE", "YEM": "YE", "DZA": "DZ", "USA": "US", "URY": "UY", "MYT": "YT", "UMI": "UM", "LBN": "LB", "LCA": "LC", "LAO": "LA", "TUV": "TV", "TWN": "TW", "TTO": "TT", "TUR": "TR", "LKA": "LK", "LIE": "LI", "LVA": "LV", "TON": "TO", "LTU": "LT", "LUX": "LU", "LBR": "LR", "LSO": "LS", "THA": "TH", "ATF": "TF", "TGO": "TG", "TCD": "TD", "TCA": "TC", "LBY": "LY", "VAT": "VA", "VCT": "VC", "ARE": "AE", "AND": "AD", "ATG": "AG", "AFG": "AF", "AIA": "AI", "VIR": "VI", "ISL": "IS", "IRN": "IR", "ARM": "AM", "ALB": "AL", "AGO": "AO", "ATA": "AQ", "ASM": "AS", "ARG": "AR", "AUS": "AU", "AUT": "AT", "ABW": "AW", "IND": "IN", "ALA": "AX", "AZE": "AZ", "IRL": "IE", "IDN": "ID", "UKR": "UA", "QAT": "QA", "MOZ": "MZ"} # TODO: Move to separate class.

    @gen.coroutine
    def _get(self):
        query_location = self.get_argument("location_id", None)
        query_cumulative = self.get_argument("cumulative", None)
        query_subadmin = self.get_argument("subadmin", None)
        query_subadmin = True if query_subadmin == "true" else False
        query_cumulative = True if query_cumulative == "true" else False
        query = {}
        if query_location is not None:
            query["query"] = parse_location_id_to_query(query_location)
        flattened_response = []
        if not query_cumulative:
            query["aggs"] = {
                "date": {
                    "terms": {
                        "field": "date_collected",
                        "size": self.size
                    }
                }
            }
            resp = yield self.asynchronous_fetch(query)
            path_to_results = ["aggregations", "date", "buckets"]
            buckets = resp
            for i in path_to_results:
                buckets = buckets[i]
            flattened_response = [{
                "date": i["key"],
                "total_count": i["doc_count"]
            } for i in buckets if not (len(i["key"].split("-")) < 3 or "XX" in i["key"])]
            flattened_response = sorted(flattened_response, key = lambda x: x["date"])
        else:
            if query_subadmin:
                subadmin = None
                if query_location is None:
                    subadmin = "country_id"
                elif len(query_location.split("_")) == 1: # Country
                    subadmin = "division_id"
                elif len(query_location.split("_")) == 2: # Division
                    subadmin = "location_id"
                query["aggs"] = {
                    "subadmin": {
                        "terms": {
                            "field": subadmin,
                            "size": self.size
                        }
                    }
                }
                resp = yield self.asynchronous_fetch(query)
                parse_id = lambda x,y: x
                if subadmin == "division_id":
                    parse_id = lambda x,loc_id: "_".join([loc_id, self.country_iso3_to_iso2[loc_id]+"-"+x if loc_id in self.country_iso3_to_iso2 else loc_id+"-"+x])
                if subadmin == "location_id":
                    parse_id = lambda x,loc_id: "_".join([loc_id, x])
                flattened_response = [{
                    "total_count": i["doc_count"],
                    "location_id": parse_id(i["key"], query_location)
                } for i in resp["aggregations"]["subadmin"]["buckets"] if i["key"].lower() != "none"]
                flattened_response = sorted(flattened_response, key = lambda x: -x["total_count"])
            else:
                resp = yield self.asynchronous_fetch(query)
                flattened_response = {
                    "total_count": get_total_hits(resp)
                }
        resp = {"success": True, "results": flattened_response}
        return resp

class GisaidIDHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
        query_id = self.get_argument("id")
        exists = False
        query = {
            "query": {
                "match": {
                    "accession_id": query_id
                }
            }
        }
        resp = yield self.asynchronous_fetch_count(query)
        if resp["count"] > 0:
            exists = True
        resp = {"success": True, "exists": exists}
        return resp

class MostRecentDateHandler(BaseHandler):
    field = "date_collected"

    @gen.coroutine
    def _get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_location = self.get_argument("location_id", None)
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
        query_pangolin_lineage = query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
        query_obj = create_nested_mutation_query(lineages = query_pangolin_lineage, mutations = query_mutations, location_id = query_location)
        query["query"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        #print(resp)
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
        return resp

class MostRecentCollectionDateHandler(MostRecentDateHandler):
    field = "date_collected"

class MostRecentSubmissionDateHandler(MostRecentDateHandler):
    field = "date_submitted"

class LocationDetailsHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
        query_str = self.get_argument("id", None)
        query_ids = query_str.split("_")
        query = {
            "query": {},
            "aggs": {
                "loc": {
                    "composite": {
                        "size": 10000,
                        "sources": []
                    }
                }
            }
        }
        loc_id_len = len(query_ids)
        if loc_id_len >= 1:
            query["aggs"]["loc"]["composite"]["sources"].extend([
                {"country": { "terms": {"field": "country"}}},
                {"country_id": { "terms": {"field": "country_id"} }}
            ])
        if loc_id_len >= 2: # 3 is max length
            query["aggs"]["loc"]["composite"]["sources"].extend([
                {"division": { "terms": {"field": "division"}}},
                {"division_id": { "terms": {"field": "division_id"} }}
            ])
        if loc_id_len == 3: # 3 is max length
            query["aggs"]["loc"]["composite"]["sources"].extend([
                {"location": { "terms": {"field": "location"}}},
                {"location_id": { "terms": {"field": "location_id"} }}
            ])
        query["query"] = parse_location_id_to_query(query_str)
        resp = yield self.asynchronous_fetch(query)
        flattened_response = []
        for rec in resp["aggregations"]["loc"]["buckets"]:
            if loc_id_len == 1:
                flattened_response.append({
                    "country": rec["key"]["country"],
                    "country_id": rec["key"]["country_id"],
                    "label": rec["key"]["country"],
                    "admin_level": 0
                })
            elif loc_id_len == 2:
                flattened_response.append({
                    "division": rec["key"]["division"],
                    "division_id": rec["key"]["division_id"],
                    "country": rec["key"]["country"],
                    "country_id": rec["key"]["country_id"],
                    "label": ", ".join([rec["key"]["division"], rec["key"]["country"]]),
                    "admin_level": 1
                })
            elif loc_id_len == 3:
                flattened_response.append({
                    "location": rec["key"]["location"],
                    "location_id": rec["key"]["location_id"],
                    "division": rec["key"]["division"],
                    "division_id": rec["key"]["division_id"],
                    "country": rec["key"]["country"],
                    "country_id": rec["key"]["country_id"],
                    "label": ", ".join([rec["key"]["location"], rec["key"]["division"], rec["key"]["country"]]),
                    "admin_level": 2
                })
        if len(flattened_response) >= 1:
            flattened_response = flattened_response[0] # ID should match only 1 region
        flattened_response["query_id"] = query_str
        resp = {"success": True, "results": flattened_response}
        return resp

class LocationHandler(BaseHandler):

    # Use dict to map to NE IDs from epi data
    country_iso3_to_iso2 = {"BGD": "BD", "BEL": "BE", "BFA": "BF", "BGR": "BG", "BIH": "BA", "BRB": "BB", "WLF": "WF", "BLM": "BL", "BMU": "BM", "BRN": "BN", "BOL": "BO", "BHR": "BH", "BDI": "BI", "BEN": "BJ", "BTN": "BT", "JAM": "JM", "BVT": "BV", "BWA": "BW", "WSM": "WS", "BES": "BQ", "BRA": "BR", "BHS": "BS", "JEY": "JE", "BLR": "BY", "BLZ": "BZ", "RUS": "RU", "RWA": "RW", "SRB": "RS", "TLS": "TL", "REU": "RE", "TKM": "TM", "TJK": "TJ", "ROU": "RO", "TKL": "TK", "GNB": "GW", "GUM": "GU", "GTM": "GT", "SGS": "GS", "GRC": "GR", "GNQ": "GQ", "GLP": "GP", "JPN": "JP", "GUY": "GY", "GGY": "GG", "GUF": "GF", "GEO": "GE", "GRD": "GD", "GBR": "GB", "GAB": "GA", "SLV": "SV", "GIN": "GN", "GMB": "GM", "GRL": "GL", "GIB": "GI", "GHA": "GH", "OMN": "OM", "TUN": "TN", "JOR": "JO", "HRV": "HR", "HTI": "HT", "HUN": "HU", "HKG": "HK", "HND": "HN", "HMD": "HM", "VEN": "VE", "PRI": "PR", "PSE": "PS", "PLW": "PW", "PRT": "PT", "SJM": "SJ", "PRY": "PY", "IRQ": "IQ", "PAN": "PA", "PYF": "PF", "PNG": "PG", "PER": "PE", "PAK": "PK", "PHL": "PH", "PCN": "PN", "POL": "PL", "SPM": "PM", "ZMB": "ZM", "ESH": "EH", "EST": "EE", "EGY": "EG", "ZAF": "ZA", "ECU": "EC", "ITA": "IT", "VNM": "VN", "SLB": "SB", "ETH": "ET", "SOM": "SO", "ZWE": "ZW", "SAU": "SA", "ESP": "ES", "ERI": "ER", "MNE": "ME", "MDA": "MD", "MDG": "MG", "MAF": "MF", "MAR": "MA", "MCO": "MC", "UZB": "UZ", "MMR": "MM", "MLI": "ML", "MAC": "MO", "MNG": "MN", "MHL": "MH", "MKD": "MK", "MUS": "MU", "MLT": "MT", "MWI": "MW", "MDV": "MV", "MTQ": "MQ", "MNP": "MP", "MSR": "MS", "MRT": "MR", "IMN": "IM", "UGA": "UG", "TZA": "TZ", "MYS": "MY", "MEX": "MX", "ISR": "IL", "FRA": "FR", "IOT": "IO", "SHN": "SH", "FIN": "FI", "FJI": "FJ", "FLK": "FK", "FSM": "FM", "FRO": "FO", "NIC": "NI", "NLD": "NL", "NOR": "NO", "NAM": "NA", "VUT": "VU", "NCL": "NC", "NER": "NE", "NFK": "NF", "NGA": "NG", "NZL": "NZ", "NPL": "NP", "NRU": "NR", "NIU": "NU", "COK": "CK", "XKX": "XK", "CIV": "CI", "CHE": "CH", "COL": "CO", "CHN": "CN", "CMR": "CM", "CHL": "CL", "CCK": "CC", "CAN": "CA", "COG": "CG", "CAF": "CF", "COD": "CD", "CZE": "CZ", "CYP": "CY", "CXR": "CX", "CRI": "CR", "CUW": "CW", "CPV": "CV", "CUB": "CU", "SWZ": "SZ", "SYR": "SY", "SXM": "SX", "KGZ": "KG", "KEN": "KE", "SSD": "SS", "SUR": "SR", "KIR": "KI", "KHM": "KH", "KNA": "KN", "COM": "KM", "STP": "ST", "SVK": "SK", "KOR": "KR", "SVN": "SI", "PRK": "KP", "KWT": "KW", "SEN": "SN", "SMR": "SM", "SLE": "SL", "SYC": "SC", "KAZ": "KZ", "CYM": "KY", "SGP": "SG", "SWE": "SE", "SDN": "SD", "DOM": "DO", "DMA": "DM", "DJI": "DJ", "DNK": "DK", "VGB": "VG", "DEU": "DE", "YEM": "YE", "DZA": "DZ", "USA": "US", "URY": "UY", "MYT": "YT", "UMI": "UM", "LBN": "LB", "LCA": "LC", "LAO": "LA", "TUV": "TV", "TWN": "TW", "TTO": "TT", "TUR": "TR", "LKA": "LK", "LIE": "LI", "LVA": "LV", "TON": "TO", "LTU": "LT", "LUX": "LU", "LBR": "LR", "LSO": "LS", "THA": "TH", "ATF": "TF", "TGO": "TG", "TCD": "TD", "TCA": "TC", "LBY": "LY", "VAT": "VA", "VCT": "VC", "ARE": "AE", "AND": "AD", "ATG": "AG", "AFG": "AF", "AIA": "AI", "VIR": "VI", "ISL": "IS", "IRN": "IR", "ARM": "AM", "ALB": "AL", "AGO": "AO", "ATA": "AQ", "ASM": "AS", "ARG": "AR", "AUS": "AU", "AUT": "AT", "ABW": "AW", "IND": "IN", "ALA": "AX", "AZE": "AZ", "IRL": "IE", "IDN": "ID", "UKR": "UA", "QAT": "QA", "MOZ": "MZ"}

    location_types = ["country", "division", "location"]

    @gen.coroutine
    def _get(self):
        query_str = self.get_argument("name", None)
        size = self.get_argument("size", None)
        flattened_response = []
        for loc in self.location_types:
            query = {
                "size": 0,
                "query": {
                    "wildcard": {
                        "{}_lower".format(loc): {
                            "value": query_str
                        }
                    }
                },
                "aggs": {
                    "loc_agg": {
                        "composite": {
                            "size": 10000,
                            "sources": [
                                {loc: { "terms": {"field": loc}}},
                                {"{}_id".format(loc): { "terms": {"field": "{}_id".format(loc)} }}
                            ]
                        }
                    }
                }
            }
            if loc == "division":
                query["aggs"]["loc_agg"]["composite"]["sources"].extend([
                    {"country": { "terms": {"field": "country"}}},
                    {"country_id": { "terms": {"field": "country_id"}}}
                ])
            if loc == "location":
                query["aggs"]["loc_agg"]["composite"]["sources"].extend([
                    {"country": { "terms": {"field": "country"}}},
                    {"country_id": { "terms": {"field": "country_id"}}},
                    {"division": { "terms": {"field": "division"}}},
                    {"division_id": { "terms": {"field": "division_id"}}}
                ])
            resp = yield self.asynchronous_fetch(query)
            if loc =="country":
                for rec in resp["aggregations"]["loc_agg"]["buckets"]:
                    flattened_response.append({
                        "country": rec["key"]["country"],
                        "country_id": rec["key"]["country_id"],
                        "id": rec["key"]["country_id"],
                        "label": rec["key"]["country"],
                        "admin_level": 0,
                        "total_count": rec["doc_count"]
                    })
            if loc =="division":
                for rec in resp["aggregations"]["loc_agg"]["buckets"]:
                    if rec["key"]["division"].lower() in ["none", "unknown"] or rec["key"]["division"].lower().replace(" ", "").replace("-", "") == "outofstate" or rec["key"]["division_id"].lower() == "none":
                        continue
                    country_iso2_code = self.country_iso3_to_iso2[rec["key"]["country_id"]] if rec["key"]["country_id"] in self.country_iso3_to_iso2 else rec["key"]["country_id"]
                    flattened_response.append({
                        "country": rec["key"]["country"],
                        "country_id": rec["key"]["country_id"],
                        "division": rec["key"]["division"],
                        "division_id": rec["key"]["division_id"],
                        "id": "_".join([rec["key"]["country_id"], country_iso2_code + "-" + rec["key"]["division_id"]]),
                        "label": ", ".join([rec["key"]["division"], rec["key"]["country"]]),
                        "admin_level": 1,
                        "total_count": rec["doc_count"]
                    })
            if loc =="location":
                for rec in resp["aggregations"]["loc_agg"]["buckets"]:
                    if rec["key"]["location"].lower() in ["none", "unknown"] or rec["key"]["location"].lower().replace(" ", "").replace("-", "") == "outofstate" or rec["key"]["location_id"].lower() == "none":
                        continue
                    country_iso2_code = self.country_iso3_to_iso2[rec["key"]["country_id"]] if rec["key"]["country_id"] in self.country_iso3_to_iso2 else rec["key"]["country_id"]
                    flattened_response.append({
                        "country": rec["key"]["country"],
                        "country_id": rec["key"]["country_id"],
                        "division": rec["key"]["division"],
                        "division_id": rec["key"]["division_id"],
                        "location": rec["key"]["location"],
                        "location_id": rec["key"]["location_id"],
                        "id": "_".join([rec["key"]["country_id"], country_iso2_code + "-" + rec["key"]["division_id"], rec["key"]["location_id"]]),
                        "label": ", ".join([rec["key"]["location"], rec["key"]["division"], rec["key"]["country"]]),
                        "admin_level": 2,
                        "total_count": rec["doc_count"]
                    })
        flattened_response = sorted(flattened_response, key = lambda x: -x["total_count"])
        if size:
            try:
                size = int(size)
            except Exception:
                return {"success": False, "results": [], "errors": "Invalide size value"}
            flattened_response = flattened_response[:size]
        resp = {"success": True, "results": flattened_response}
        return resp

class MutationHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
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
        return resp

class SubmissionLagHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
        query_location = self.get_argument("location_id", None)
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
        if query_location is not None:
            query["query"] = parse_location_id_to_query(query_location)
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
        return resp

class MetadataHandler(BaseHandler):

    @gen.coroutine
    def _get(self):
        mapping = yield self.get_mapping()
        
        # mapping dict key is name of index, unknown here.
        mapping = [val for val in mapping.values()][0]['mappings']
        res = None
        if "mutation" in mapping:
            res = mapping['mutation']['_meta']
        else:
            res = mapping["_meta"]
        return res
