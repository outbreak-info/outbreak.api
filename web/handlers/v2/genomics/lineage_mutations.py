import re

import pandas as pd

from web.handlers.genomics.base import BaseHandler


class LineageMutationsHandler(BaseHandler):
    gene_mapping = {
        "orf1a": "ORF1a",
        "orf1b": "ORF1b",
        "s": "S",
        "orf3a": "ORF3a",
        "e": "E",
        "m": "M",
        "orf6": "ORF6",
        "orf7a": "ORF7a",
        "orf7b": "ORF7b",
        "orf8": "ORF8",
        "n": "N",
        "orf10": "ORF10",
    }

    name = "lineage-mutations"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str, "required": True},
        "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
        "gene": {"type": str, "default": None},
    }

    async def _get(self):
        pangolin_lineage = self.args.pangolin_lineage
        frequency = self.args.frequency
        gene = self.args.gene
        if gene:
            genes = gene.lower().split(",")
        else:
            genes = []
        dict_response = {}

        query_lineages = " OR ".join(pangolin_lineage.split(","))

        query = {"size": 0,
                    "track_total_hits": True,
                    "query": {
                        "bool": {
                            "filter": [
                                {
                                    "query_string": {
                                        "default_field": "pangolin_lineage.keyword",
                                        # Ex: "query": "BA.1.* OR BA.2"
                                        "query": query_lineages
                                    }
                                }
                            ]
                        }
                    },
                    "aggs": {
                        "lineages": {
                            "terms": {
                                "field": "pangolin_lineage.keyword"
                            },
                            "aggs": {
                                "mutations": {
                                    "terms": {
                                        "field": "mutations.keyword",
                                        "size": 10000
                                    }
                                }
                            }
                        }
                    }
                }

        self.observability.log("es_query_before", query)

        resp = await self.asynchronous_fetch(query)

        self.observability.log("es_query_after", query)

        for lineage in resp["aggregations"]["lineages"]["buckets"]:
            path_to_results = ["mutations", "buckets"]

            buckets = lineage
            for i in path_to_results:
                buckets = buckets[i]
            flattened_response = [
                {
                    "mutation": i["key"],
                    "mutation_count": i["doc_count"],
                    "lineage_count": lineage["doc_count"],
                    "lineage": lineage["key"],
                }
                for i in buckets
            ]

            if len(flattened_response) > 0:
                df_response = pd.DataFrame(flattened_response).assign(
                    gene=lambda x: x["mutation"].apply(
                        lambda k: self.gene_mapping[k.split(":")[0]]
                        if k.split(":")[0] in self.gene_mapping
                        else k.split(":")[0]
                    ),
                    ref_aa=lambda x: x["mutation"]
                    .apply(
                        lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[0]
                        if "DEL" not in k and "del" not in k and "_" not in k
                        else k
                    )
                    .str.upper(),
                    alt_aa=lambda x: x["mutation"]
                    .apply(
                        lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[1]
                        if "DEL" not in k and "del" not in k and "_" not in k
                        else k.split(":")[1]
                    )
                    .str.upper(),
                    codon_num=lambda x: x["mutation"].apply(
                        lambda k: int(re.findall("[0-9]+", k.split(":")[1])[0])
                    ),
                    codon_end=lambda x: x["mutation"].apply(
                        lambda k: int(re.findall("[0-9]+", k.split(":")[1])[1])
                        if "/" in k and ("DEL" in k or "del" in k)
                        else None
                    ),
                    type=lambda x: x["mutation"].apply(
                        lambda k: "deletion" if "DEL" in k or "del" in k else "substitution"
                    ),
                )
                df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
                df_response.loc[:, "prevalence"] = (
                    df_response["mutation_count"] / df_response["lineage_count"]
                )
                df_response.loc[~df_response["codon_end"].isna(), "change_length_nt"] = (
                    (df_response["codon_end"] - df_response["codon_num"]) + 1
                ) * 3
                df_response = df_response[df_response["prevalence"] >= frequency].fillna("None")
                if genes:
                    df_response = df_response[df_response["gene"].str.lower().isin(genes)]
                dict_response[lineage["key"]] = df_response.to_dict(orient="records")

        self.observability.log("transformations_after")

        result = {"success": True, "results": dict_response}
        return result
