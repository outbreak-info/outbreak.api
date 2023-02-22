from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import get_total_hits, parse_location_id_to_query


class SequenceCountHandler(BaseHandler):
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
    name = "sequence-count"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "location_id": {"type": str, "default": None},
        "cumulative": {"type": bool, "default": False},
        "subadmin": {"type": bool, "default": False},
    }

    async def _get(self):
        query_location = self.args.location_id
        query_cumulative = self.args.cumulative
        query_subadmin = self.args.subadmin
        query = {}
        if query_location is not None:
            query["query"] = parse_location_id_to_query(query_location)
        if not query_cumulative:
            query["aggs"] = {"date": {"terms": {"field": "date_collected", "size": self.size}}}
            resp = await self.asynchronous_fetch(query)
            path_to_results = ["aggregations", "date", "buckets"]
            buckets = resp
            for i in path_to_results:
                buckets = buckets[i]
            flattened_response = [
                {"date": i["key"], "total_count": i["doc_count"]}
                for i in buckets
                if not (len(i["key"].split("-")) < 3 or "XX" in i["key"])
            ]
            flattened_response = sorted(flattened_response, key=lambda x: x["date"])
        else:
            if query_subadmin:
                subadmin = None
                if query_location is None:
                    subadmin = "country_id"
                elif len(query_location.split("_")) == 1:  # Country
                    subadmin = "division_id"
                elif len(query_location.split("_")) == 2:  # Division
                    subadmin = "location_id"
                query["aggs"] = {"subadmin": {"terms": {"field": subadmin, "size": self.size}}}
                resp = await self.asynchronous_fetch(query)
                parse_id = lambda x, y: x
                if subadmin == "division_id":
                    parse_id = lambda x, loc_id: "_".join(
                        [
                            loc_id,
                            self.country_iso3_to_iso2[loc_id] + "-" + x
                            if loc_id in self.country_iso3_to_iso2
                            else loc_id + "-" + x,
                        ]
                    )
                if subadmin == "location_id":
                    parse_id = lambda x, loc_id: "_".join([loc_id, x])
                flattened_response = [
                    {
                        "total_count": i["doc_count"],
                        "location_id": parse_id(i["key"], query_location),
                    }
                    for i in resp["aggregations"]["subadmin"]["buckets"]
                    if i["key"].lower() != "none"
                ]
                flattened_response = sorted(flattened_response, key=lambda x: -x["total_count"])
            else:
                resp = await self.asynchronous_fetch(query)
                flattened_response = {"total_count": get_total_hits(resp)}
        resp = {"success": True, "results": flattened_response}
        return resp
