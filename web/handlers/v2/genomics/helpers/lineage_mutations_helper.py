import pandas as pd
import re

def gene_mapping():    
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

def create_query(pangolin_lineage = []):
    query_lineages = ""
    for lineage_param in re.split(r',| OR ', pangolin_lineage):
        lineage_ands = lineage_param.split(" AND ")
        lineage_ors = lineage_param.split(" OR ")
        if len(lineage_ands) > 1:
            if query_lineages != "":
                query_lineages = query_lineages + " OR "
            query_lineages = query_lineages + "(pangolin_lineage.keyword: " + lineage_ands[0] + " AND mutations.keyword: "
            modified_mutations = ["\\:".join(mutation.split(":")) if ":" in mutation else mutation for mutation in lineage_ands[1:]]
            query_mutations = " AND mutations.keyword: ".join(modified_mutations)
            query_lineages = query_lineages + query_mutations
            query_lineages = query_lineages + ")"
        elif len(lineage_ors) > 1:
            if query_lineages != "":
                query_lineages = query_lineages + " OR "
            query_lineages = "pangolin_lineage.keyword: " + lineage_ors[0] + " OR mutations: "
            query_mutations = " OR pangolin_lineage.keyword: ".join(lineage_ors[1:])
            query_lineages = query_lineages + query_mutations
        else:
            if query_lineages != "":
                query_lineages = query_lineages + " OR "
            query_lineages = query_lineages + "(pangolin_lineage.keyword: " + lineage_param + ")"

    query = {"size": 0,
                "track_total_hits": True,
                "query": {
                    "bool": {
                        "filter": [
                            {
                                "query_string": {
                                    # Ex: "query": "(pangolin_lineage.keyword: BA.1 OR pangolin_lineage.keyword: BA.1.1) OR (pangolin_lineage.keyword: BA.2 AND mutations: 'S\\:D614G')"
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
                                    "size": 2
                                }
                            }
                        }
                    }
                }
            }

    return query

def parse_response(resp = {}, frequency = 1, genes = []):
    dict_response = {}
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
            df_response = df_response[df_response["prevalence"] >= frequency].fillna("None")
            if genes:
                df_response = df_response[df_response["gene"].str.lower().isin(genes)]
            dict_response[lineage["key"]] = df_response.to_dict(orient="records")
    return dict_response
