from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import (
    create_iterator,
    create_nested_mutation_query,
    parse_location_id_to_query,
    transform_prevalence_by_location_and_tiime,
)


class CumulativePrevalenceByLocationHandler(BaseHandler):
    name = "lineage-by-sub-admin-most-recent"

    country_iso3_to_iso2 = {
        "BGD": "BD",
        "BEL": "BE",
        "BFA": "BF",
        "BGR": "BG",
        "BIH": "BA",
        "BRB": "BB",
        "WLF": "WF",
        "BLM": "BL",
        "BMU": "BM",
        "BRN": "BN",
        "BOL": "BO",
        "BHR": "BH",
        "BDI": "BI",
        "BEN": "BJ",
        "BTN": "BT",
        "JAM": "JM",
        "BVT": "BV",
        "BWA": "BW",
        "WSM": "WS",
        "BES": "BQ",
        "BRA": "BR",
        "BHS": "BS",
        "JEY": "JE",
        "BLR": "BY",
        "BLZ": "BZ",
        "RUS": "RU",
        "RWA": "RW",
        "SRB": "RS",
        "TLS": "TL",
        "REU": "RE",
        "TKM": "TM",
        "TJK": "TJ",
        "ROU": "RO",
        "TKL": "TK",
        "GNB": "GW",
        "GUM": "GU",
        "GTM": "GT",
        "SGS": "GS",
        "GRC": "GR",
        "GNQ": "GQ",
        "GLP": "GP",
        "JPN": "JP",
        "GUY": "GY",
        "GGY": "GG",
        "GUF": "GF",
        "GEO": "GE",
        "GRD": "GD",
        "GBR": "GB",
        "GAB": "GA",
        "SLV": "SV",
        "GIN": "GN",
        "GMB": "GM",
        "GRL": "GL",
        "GIB": "GI",
        "GHA": "GH",
        "OMN": "OM",
        "TUN": "TN",
        "JOR": "JO",
        "HRV": "HR",
        "HTI": "HT",
        "HUN": "HU",
        "HKG": "HK",
        "HND": "HN",
        "HMD": "HM",
        "VEN": "VE",
        "PRI": "PR",
        "PSE": "PS",
        "PLW": "PW",
        "PRT": "PT",
        "SJM": "SJ",
        "PRY": "PY",
        "IRQ": "IQ",
        "PAN": "PA",
        "PYF": "PF",
        "PNG": "PG",
        "PER": "PE",
        "PAK": "PK",
        "PHL": "PH",
        "PCN": "PN",
        "POL": "PL",
        "SPM": "PM",
        "ZMB": "ZM",
        "ESH": "EH",
        "EST": "EE",
        "EGY": "EG",
        "ZAF": "ZA",
        "ECU": "EC",
        "ITA": "IT",
        "VNM": "VN",
        "SLB": "SB",
        "ETH": "ET",
        "SOM": "SO",
        "ZWE": "ZW",
        "SAU": "SA",
        "ESP": "ES",
        "ERI": "ER",
        "MNE": "ME",
        "MDA": "MD",
        "MDG": "MG",
        "MAF": "MF",
        "MAR": "MA",
        "MCO": "MC",
        "UZB": "UZ",
        "MMR": "MM",
        "MLI": "ML",
        "MAC": "MO",
        "MNG": "MN",
        "MHL": "MH",
        "MKD": "MK",
        "MUS": "MU",
        "MLT": "MT",
        "MWI": "MW",
        "MDV": "MV",
        "MTQ": "MQ",
        "MNP": "MP",
        "MSR": "MS",
        "MRT": "MR",
        "IMN": "IM",
        "UGA": "UG",
        "TZA": "TZ",
        "MYS": "MY",
        "MEX": "MX",
        "ISR": "IL",
        "FRA": "FR",
        "IOT": "IO",
        "SHN": "SH",
        "FIN": "FI",
        "FJI": "FJ",
        "FLK": "FK",
        "FSM": "FM",
        "FRO": "FO",
        "NIC": "NI",
        "NLD": "NL",
        "NOR": "NO",
        "NAM": "NA",
        "VUT": "VU",
        "NCL": "NC",
        "NER": "NE",
        "NFK": "NF",
        "NGA": "NG",
        "NZL": "NZ",
        "NPL": "NP",
        "NRU": "NR",
        "NIU": "NU",
        "COK": "CK",
        "XKX": "XK",
        "CIV": "CI",
        "CHE": "CH",
        "COL": "CO",
        "CHN": "CN",
        "CMR": "CM",
        "CHL": "CL",
        "CCK": "CC",
        "CAN": "CA",
        "COG": "CG",
        "CAF": "CF",
        "COD": "CD",
        "CZE": "CZ",
        "CYP": "CY",
        "CXR": "CX",
        "CRI": "CR",
        "CUW": "CW",
        "CPV": "CV",
        "CUB": "CU",
        "SWZ": "SZ",
        "SYR": "SY",
        "SXM": "SX",
        "KGZ": "KG",
        "KEN": "KE",
        "SSD": "SS",
        "SUR": "SR",
        "KIR": "KI",
        "KHM": "KH",
        "KNA": "KN",
        "COM": "KM",
        "STP": "ST",
        "SVK": "SK",
        "KOR": "KR",
        "SVN": "SI",
        "PRK": "KP",
        "KWT": "KW",
        "SEN": "SN",
        "SMR": "SM",
        "SLE": "SL",
        "SYC": "SC",
        "KAZ": "KZ",
        "CYM": "KY",
        "SGP": "SG",
        "SWE": "SE",
        "SDN": "SD",
        "DOM": "DO",
        "DMA": "DM",
        "DJI": "DJ",
        "DNK": "DK",
        "VGB": "VG",
        "DEU": "DE",
        "YEM": "YE",
        "DZA": "DZ",
        "USA": "US",
        "URY": "UY",
        "MYT": "YT",
        "UMI": "UM",
        "LBN": "LB",
        "LCA": "LC",
        "LAO": "LA",
        "TUV": "TV",
        "TWN": "TW",
        "TTO": "TT",
        "TUR": "TR",
        "LKA": "LK",
        "LIE": "LI",
        "LVA": "LV",
        "TON": "TO",
        "LTU": "LT",
        "LUX": "LU",
        "LBR": "LR",
        "LSO": "LS",
        "THA": "TH",
        "ATF": "TF",
        "TGO": "TG",
        "TCD": "TD",
        "TCA": "TC",
        "LBY": "LY",
        "VAT": "VA",
        "VCT": "VC",
        "ARE": "AE",
        "AND": "AD",
        "ATG": "AG",
        "AFG": "AF",
        "AIA": "AI",
        "VIR": "VI",
        "ISL": "IS",
        "IRN": "IR",
        "ARM": "AM",
        "ALB": "AL",
        "AGO": "AO",
        "ATA": "AQ",
        "ASM": "AS",
        "ARG": "AR",
        "AUS": "AU",
        "AUT": "AT",
        "ABW": "AW",
        "IND": "IN",
        "ALA": "AX",
        "AZE": "AZ",
        "IRL": "IE",
        "IDN": "ID",
        "UKR": "UA",
        "QAT": "QA",
        "MOZ": "MZ",
    }  # TODO: Move to separate class.
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str, "required": True},
        "detected": {"type": bool, "default": False},
        "mutations": {"type": str, "default": None},
        "location_id": {"type": str, "default": None},
        "ndays": {"type": int, "default": None, "min": 1},
    }

    async def _get(self):
        query_pangolin_lineage = self.args.pangolin_lineage
        query_pangolin_lineage = (
            query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
        )
        query_detected = self.args.detected
        query_mutations = self.args.mutations
        query_location = self.args.location_id
        query_mutations = query_mutations.split(" AND ") if query_mutations is not None else []
        query_ndays = self.args.ndays
        results = {}
        for query_lineage, query_mutation in create_iterator(
            query_pangolin_lineage, query_mutations
        ):
            query = {
                "size": 0,
                "aggs": {
                    "sub_date_buckets": {
                        "composite": {
                            "size": 10000,
                            "sources": [{"date_collected": {"terms": {"field": "date_collected"}}}],
                        },
                        "aggregations": {"lineage_count": {"filter": {}}},
                    }
                },
            }
            if query_location is not None:  # Global
                query["query"] = parse_location_id_to_query(query_location)
            admin_level = 0
            if query_location is None:
                query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend(
                    [
                        {"sub": {"terms": {"field": "country"}}},
                        {"sub_id": {"terms": {"field": "country_id"}}},
                    ]
                )
                admin_level = 0
            elif len(query_location.split("_")) == 2:
                query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend(
                    [
                        {"sub_id": {"terms": {"field": "location_id"}}},
                        {"sub": {"terms": {"field": "location"}}},
                    ]
                )
                admin_level = 2
            elif len(query_location.split("_")) == 1:
                query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend(
                    [
                        {"sub_id": {"terms": {"field": "division_id"}}},
                        {"sub": {"terms": {"field": "division"}}},
                    ]
                )
                admin_level = 1
            query_lineages = query_lineage.split(" OR ") if query_lineage is not None else []
            query_obj = create_nested_mutation_query(
                lineages=query_lineages, mutations=query_mutation
            )
            query["aggs"]["sub_date_buckets"]["aggregations"]["lineage_count"]["filter"] = query_obj
            resp = await self.asynchronous_fetch(query)
            buckets = resp["aggregations"]["sub_date_buckets"]["buckets"]
            # Get all paginated results
            while "after_key" in resp["aggregations"]["sub_date_buckets"]:
                query["aggs"]["sub_date_buckets"]["composite"]["after"] = resp["aggregations"][
                    "sub_date_buckets"
                ]["after_key"]
                resp = await self.asynchronous_fetch(query)
                buckets.extend(resp["aggregations"]["sub_date_buckets"]["buckets"])
            dict_response = {}
            if len(buckets) > 0:
                flattened_response = []
                for i in buckets:
                    if (
                        len(i["key"]["date_collected"].split("-")) < 3
                        or "XX" in i["key"]["date_collected"]
                    ):
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
                        "lineage_count": i["lineage_count"]["doc_count"],
                    }
                    if admin_level == 1:
                        rec["id"] = "_".join(
                            [
                                query_location,
                                self.country_iso3_to_iso2[query_location] + "-" + i["key"]["sub_id"]
                                if query_location in self.country_iso3_to_iso2
                                else query_location + "-" + i["key"]["sub_id"],
                            ]
                        )
                    elif admin_level == 2:
                        rec["id"] = "_".join([query_location, i["key"]["sub_id"]])
                    flattened_response.append(rec)
                dict_response = transform_prevalence_by_location_and_tiime(
                    flattened_response, query_ndays, query_detected
                )
            res_key = None
            if (
                query_lineage is not None
            ):  # create_iterator will never return empty list for lineages
                res_key = " OR ".join(query_lineages)
            if len(query_mutations) > 0:
                res_key = (
                    "({}) AND ({})".format(res_key, " AND ".join(query_mutations))
                    if res_key is not None
                    else " AND ".join(query_mutations)
                )
            results[res_key] = dict_response
        return {"success": True, "results": results}
