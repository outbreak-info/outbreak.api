import re
from typing import Dict, List, Optional

import pandas as pd


def gene_mapping() -> Dict:
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
    return gene_mapping


def parse_response(
    resp: Dict = None, frequency: int = 1, lineages: str = "", genes: Optional[List[str]] = None
) -> Dict:
    dict_response = {}

    lineage = resp["aggregations"]
    if len(lineages) > 0:
        lineage["key"] = lineages

    path_to_results = ["mutations", "buckets"]

    buckets = lineage
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = [
        {
            "mutation": i["key"],
            "mutation_count": i["doc_count"],
            "lineage_count": resp["hits"]["total"]["value"],
            "lineage": lineage["key"],
        }
        for i in buckets
    ]

    if len(flattened_response) > 0:
        df_response = pd.DataFrame(flattened_response).assign(
            gene=lambda x: x["mutation"].apply(
                lambda k: gene_mapping()[k.split(":")[0]]
                if k.split(":")[0] in gene_mapping()
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
        df_response = (
            df_response[df_response["prevalence"] >= frequency]
            .fillna(pd.NA)
            .replace([pd.NA], [None])
        )
        if genes:
            df_response = df_response[df_response["gene"].str.lower().isin(genes)]
        dict_response[lineage["key"]] = df_response.to_dict(orient="records")
    return dict_response


def parse_response_q(resp: Dict = None, idx: int = 0, params: Dict = None) -> Dict:
    dict_response = {}

    lineage = resp["aggregations"]
    lineage["key"] = params["q_list"][idx]

    frequency = params["frequency"]
    genes = params["genes"]

    path_to_results = ["mutations", "buckets"]

    buckets = lineage
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = [
        {
            "mutation": i["key"],
            "mutation_count": i["doc_count"],
            "lineage_count": resp["hits"]["total"]["value"],
            "lineage": lineage["key"],
        }
        for i in buckets
    ]

    if len(flattened_response) > 0:
        df_response = pd.DataFrame(flattened_response).assign(
            gene=lambda x: x["mutation"].apply(
                lambda k: gene_mapping()[k.split(":")[0]]
                if k.split(":")[0] in gene_mapping()
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
        df_response = (
            df_response[df_response["prevalence"] >= frequency]
            .fillna(pd.NA)
            .replace([pd.NA], [None])
        )
        if genes:
            df_response = df_response[df_response["gene"].str.lower().isin(genes)]
        dict_response[lineage["key"]] = df_response.to_dict(orient="records")
    return dict_response
