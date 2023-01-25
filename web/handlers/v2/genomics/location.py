from web.handlers.genomics.base import BaseHandler


class LocationHandler(BaseHandler):

    # Use dict to map to NE IDs from epi data
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
    }

    location_types = ["country", "division", "location"]
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "name": {"type": str, "default": None},
        "size": {"type": int, "default": None},
    }

    async def _get(self):
        query_str = self.args.name
        size = self.args.size
        flattened_response = []
        for loc in self.location_types:
            query = {
                "size": 0,
                "query": {"wildcard": {"{}_lower".format(loc): {"value": query_str}}},
                "aggs": {
                    "loc_agg": {
                        "composite": {
                            "size": 10000,
                            "sources": [
                                {loc: {"terms": {"field": loc}}},
                                {"{}_id".format(loc): {"terms": {"field": "{}_id".format(loc)}}},
                            ],
                        }
                    }
                },
            }
            if loc == "division":
                query["aggs"]["loc_agg"]["composite"]["sources"].extend(
                    [
                        {"country": {"terms": {"field": "country"}}},
                        {"country_id": {"terms": {"field": "country_id"}}},
                    ]
                )
            if loc == "location":
                query["aggs"]["loc_agg"]["composite"]["sources"].extend(
                    [
                        {"country": {"terms": {"field": "country"}}},
                        {"country_id": {"terms": {"field": "country_id"}}},
                        {"division": {"terms": {"field": "division"}}},
                        {"division_id": {"terms": {"field": "division_id"}}},
                    ]
                )
            resp = await self.asynchronous_fetch(query)
            if loc == "country":
                for rec in resp["aggregations"]["loc_agg"]["buckets"]:
                    flattened_response.append(
                        {
                            "country": rec["key"]["country"],
                            "country_id": rec["key"]["country_id"],
                            "id": rec["key"]["country_id"],
                            "label": rec["key"]["country"],
                            "admin_level": 0,
                            "total_count": rec["doc_count"],
                        }
                    )
            if loc == "division":
                for rec in resp["aggregations"]["loc_agg"]["buckets"]:
                    if (
                        rec["key"]["division"].lower() in ["none", "unknown"]
                        or rec["key"]["division"].lower().replace(" ", "").replace("-", "")
                        == "outofstate"
                        or rec["key"]["division_id"].lower() == "none"
                    ):
                        continue
                    country_iso2_code = (
                        self.country_iso3_to_iso2[rec["key"]["country_id"]]
                        if rec["key"]["country_id"] in self.country_iso3_to_iso2
                        else rec["key"]["country_id"]
                    )
                    flattened_response.append(
                        {
                            "country": rec["key"]["country"],
                            "country_id": rec["key"]["country_id"],
                            "division": rec["key"]["division"],
                            "division_id": rec["key"]["division_id"],
                            "id": "_".join(
                                [
                                    rec["key"]["country_id"],
                                    country_iso2_code + "-" + rec["key"]["division_id"],
                                ]
                            ),
                            "label": ", ".join([rec["key"]["division"], rec["key"]["country"]]),
                            "admin_level": 1,
                            "total_count": rec["doc_count"],
                        }
                    )
            if loc == "location":
                for rec in resp["aggregations"]["loc_agg"]["buckets"]:
                    if (
                        rec["key"]["location"].lower() in ["none", "unknown"]
                        or rec["key"]["location"].lower().replace(" ", "").replace("-", "")
                        == "outofstate"
                        or rec["key"]["location_id"].lower() == "none"
                    ):
                        continue
                    country_iso2_code = (
                        self.country_iso3_to_iso2[rec["key"]["country_id"]]
                        if rec["key"]["country_id"] in self.country_iso3_to_iso2
                        else rec["key"]["country_id"]
                    )
                    flattened_response.append(
                        {
                            "country": rec["key"]["country"],
                            "country_id": rec["key"]["country_id"],
                            "division": rec["key"]["division"],
                            "division_id": rec["key"]["division_id"],
                            "location": rec["key"]["location"],
                            "location_id": rec["key"]["location_id"],
                            "id": "_".join(
                                [
                                    rec["key"]["country_id"],
                                    country_iso2_code + "-" + rec["key"]["division_id"],
                                    rec["key"]["location_id"],
                                ]
                            ),
                            "label": ", ".join(
                                [
                                    rec["key"]["location"],
                                    rec["key"]["division"],
                                    rec["key"]["country"],
                                ]
                            ),
                            "admin_level": 2,
                            "total_count": rec["doc_count"],
                        }
                    )
        flattened_response = sorted(flattened_response, key=lambda x: -x["total_count"])
        if size:
            try:
                size = int(size)
            except Exception:
                return {"success": False, "results": [], "errors": "Invalide size value"}
            flattened_response = flattened_response[:size]
        resp = {"success": True, "results": flattened_response}
        return resp
