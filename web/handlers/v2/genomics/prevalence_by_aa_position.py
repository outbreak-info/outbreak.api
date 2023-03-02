import pandas as pd

from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import compute_rolling_mean, parse_location_id_to_query


class PrevalenceByAAPositionHandler(BaseHandler):
    name = "prevalence-by-position"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str, "default": None},
        "location_id": {"type": str, "default": None},
        "name": {"type": str, "required": True},  # should be deprecated
        "gene": {
            "type": str,
            "required": False,
        },  # replacement of name parameter for validator applying
        "position": {
            "type": int,
            "required": False,
        },  # replacement of name parameter for validator applying
    }

    async def _get(self):
        query_str = self.args.name
        query_location = self.args.location_id
        query_lineage = self.args.pangolin_lineage
        query_gene = self.args.gene
        if not query_gene:
            query_gene = query_str.split(":")[0]
        query_aa_position = self.args.position
        if query_aa_position is None:
            query_aa_position = int(query_str.split(":")[1])
        # Get ref codon
        query = {
            "size": 0,
            "aggs": {
                "by_mutations": {
                    "nested": {"path": "mutations"},
                    "aggs": {
                        "inner": {
                            "filter": {
                                "bool": {
                                    "must": [
                                        {"match": {"mutations.codon_num": query_aa_position}},
                                        {"match": {"mutations.gene": query_gene}},
                                    ]
                                }
                            },
                            "aggs": {"by_nested": {"top_hits": {"size": 1}}},
                        }
                    },
                }
            },
        }
        resp = await self.asynchronous_fetch(query)
        tmp_ref = resp["aggregations"]["by_mutations"]["inner"]["by_nested"]["hits"]["hits"]
        dict_response = []
        if len(tmp_ref) > 0:
            ref_aa = tmp_ref[0]["_source"]["ref_aa"]
            query = {
                "aggs": {
                    "by_date": {
                        "terms": {"field": "date_collected", "size": self.size},
                        "aggs": {
                            "by_mutations": {
                                "nested": {"path": "mutations"},
                                "aggs": {
                                    "inner": {
                                        "filter": {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "match": {
                                                            "mutations.codon_num": query_aa_position
                                                        }
                                                    },
                                                    {"match": {"mutations.gene": query_gene}},
                                                ]
                                            }
                                        },
                                        "aggs": {
                                            "by_name": {"terms": {"field": "mutations.alt_aa"}}
                                        },
                                    }
                                },
                            }
                        },
                    }
                }
            }
            if query_location is not None:
                query["query"] = parse_location_id_to_query(
                    query_location, query["aggs"]["prevalence"]["filter"]
                )
            if query_lineage is not None:
                if "query" in query:
                    query["query"]["bool"]["must"].append(
                        {"term": {"pangolin_lineage": query_lineage}}
                    )
                else:
                    query["query"] = {"term": {"pangolin_lineage": query_lineage}}
            resp = await self.asynchronous_fetch(query)
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
                    flattened_response.append(
                        {
                            "date": d["key"],
                            "total_count": d["doc_count"],
                            "aa": m["key"],
                            "aa_count": m["doc_count"],
                        }
                    )
                    alt_count += m["doc_count"]
                flattened_response.append(
                    {
                        "date": d["key"],
                        "total_count": d["doc_count"],
                        "aa": ref_aa,
                        "aa_count": d["doc_count"] - alt_count,
                    }
                )
            df_response = (
                pd.DataFrame(flattened_response)
                .assign(
                    date=lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"),
                    prevalence=lambda x: x["aa_count"] / x["total_count"],
                )
                .sort_values("date")
            )
            df_response = df_response.groupby("aa").apply(
                compute_rolling_mean, "date", "prevalence", "prevalence_rolling"
            )
            df_response.loc[:, "date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
            dict_response = df_response.to_dict(orient="records")
        resp = {"success": True, "results": dict_response}
        return resp
