# #############################
# ### TheadPool

# import re
# import asyncio
# import pandas as pd
# import concurrent.futures
# from web.handlers.genomics.base import BaseHandler
# from web.handlers.genomics.util import create_nested_mutation_query, get_total_hits


# class LineageMutationsHandler(BaseHandler):
#     gene_mapping = {
#         "orf1a": "ORF1a",
#         "orf1b": "ORF1b",
#         "s": "S",
#         "orf3a": "ORF3a",
#         "e": "E",
#         "m": "M",
#         "orf6": "ORF6",
#         "orf7a": "ORF7a",
#         "orf7b": "ORF7b",
#         "orf8": "ORF8",
#         "n": "N",
#         "orf10": "ORF10",
#     }

#     name = "lineage-mutations"
#     kwargs = dict(BaseHandler.kwargs)
#     kwargs["GET"] = {
#         "pangolin_lineage": {"type": str, "required": True},
#         "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
#         "gene": {"type": str, "default": None},
#     }

#     async def process_query(self, query_lineage, frequency, genes, dict_response):
#         # Function to process the query for a single lineage
#         query = {
#             "size": 0,
#             "query": {},
#             "aggs": {
#                 "mutations": {
#                     "nested": {"path": "mutations"},
#                     "aggs": {
#                         "mutations": {
#                             "terms": {"field": "mutations.mutation", "size": 10000},
#                             "aggs": {"genomes": {"reverse_nested": {}}},
#                         }
#                     },
#                 }
#             },
#         }
#         query_lineage_split = query_lineage.split(" AND ")
#         query_mutations = []
#         query_pangolin_lineage = query_lineage_split[0].split(" OR ")
#         if len(query_lineage_split) > 1:
#             query_mutations = query_lineage_split[1:]
#         query["query"] = create_nested_mutation_query(
#             lineages=query_pangolin_lineage, mutations=query_mutations
#         )

#         self.observability.log("es_query_before", query)

#         resp = await self.asynchronous_fetch(query)

#         self.observability.log("es_query_after", query)

#         path_to_results = ["aggregations", "mutations", "mutations", "buckets"]
#         buckets = resp
#         for i in path_to_results:
#             buckets = buckets[i]
#         flattened_response = [
#             {
#                 "mutation": i["key"],
#                 "mutation_count": i["genomes"]["doc_count"],
#                 "lineage_count": get_total_hits(resp),
#                 "lineage": query_lineage,
#             }
#             for i in buckets
#         ]
#         if len(flattened_response) > 0:
#             df_response = pd.DataFrame(flattened_response).assign(
#                 gene=lambda x: x["mutation"].apply(
#                     lambda k: re.findall("[A-Za-z*]+", k.split(":")[0])[0]
#                 ).map(LineageMutationsHandler.gene_mapping),
#                 ref_aa=lambda x: x["mutation"]
#                 .apply(
#                     lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[0]
#                     if "DEL" not in k and "del" not in k and "_" not in k
#                     else k
#                 )
#                 .str.upper(),
#                 alt_aa=lambda x: x["mutation"]
#                 .apply(
#                     lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[1]
#                     if "DEL" not in k and "del" not in k and "_" not in k
#                     else k.split(":")[1]
#                 )
#                 .str.upper(),
#                 codon_num=lambda x: x["mutation"].apply(
#                     lambda k: int(re.findall("[0-9]+", k.split(":")[1])[0])
#                 ),
#                 codon_end=lambda x: x["mutation"].apply(
#                     lambda k: int(re.findall("[0-9]+", k.split(":")[1])[1])
#                     if "/" in k and ("DEL" in k or "del" in k)
#                     else None
#                 ),
#                 type=lambda x: x["mutation"].apply(
#                     lambda k: "deletion" if "DEL" in k or "del" in k else "substitution"
#                 ),
#             )
#             df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
#             df_response.loc[:, "prevalence"] = (
#                 df_response["mutation_count"] / df_response["lineage_count"]
#             )
#             df_response.loc[~df_response["codon_end"].isna(), "change_length_nt"] = (
#                 (df_response["codon_end"] - df_response["codon_num"]) + 1
#             ) * 3
#             df_response = df_response[df_response["prevalence"] >= frequency].fillna("None")
#             if genes:
#                 df_response = df_response[df_response["gene"].str.lower().isin(genes)]
#             dict_response[query_lineage] = df_response.to_dict(orient="records")

#         self.observability.log("transformations")

#     async def _get(self):
#         self.observability.log("function_get", self.args)
#         self.observability.lock_time()
#         pangolin_lineage = self.args.pangolin_lineage
#         frequency = self.args.frequency
#         gene = self.args.gene
#         if gene:
#             genes = gene.lower().split(",")
#         else:
#             genes = []
#         dict_response = {}

#         tasks = [(query_lineage, frequency, genes, dict_response) for query_lineage in pangolin_lineage.split(",")]

#         # Create a thread pool executor
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             # Execute the queries in parallel
#             await asyncio.gather(*(self.process_query(*args) for args in tasks))

#         self.observability.release_time()

#         resp = {"success": True, "results": dict_response}

#         self.observability.log("before_return")

#         return resp


# #######################
# ##### ASYNC

# import asyncio
# import pandas as pd
# import re

# from web.handlers.genomics.base import BaseHandler
# from web.handlers.genomics.util import create_nested_mutation_query, get_total_hits


# class LineageMutationsHandler(BaseHandler):

#     gene_mapping = {
#         "orf1a": "ORF1a",
#         "orf1b": "ORF1b",
#         "s": "S",
#         "orf3a": "ORF3a",
#         "e": "E",
#         "m": "M",
#         "orf6": "ORF6",
#         "orf7a": "ORF7a",
#         "orf7b": "ORF7b",
#         "orf8": "ORF8",
#         "n": "N",
#         "orf10": "ORF10",
#     }

#     name = "lineage-mutations"
#     kwargs = dict(BaseHandler.kwargs)
#     kwargs["GET"] = {
#         "pangolin_lineage": {"type": str, "required": True},
#         "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
#         "gene": {"type": str, "default": None},
#     }


#     async def _get(self):
#         self.observability.log("function_get", self.args)
#         self.observability.lock_time()
#         pangolin_lineage = self.args.pangolin_lineage
#         frequency = self.args.frequency
#         gene = self.args.gene
#         if gene:
#             genes = gene.lower().split(",")
#         else:
#             genes = []
#         dict_response = {}

#         async def process_query(query_lineage):
#             query = {
#                 "size": 0,
#                 "query": {},
#                 "aggs": {
#                     "mutations": {
#                         "nested": {"path": "mutations"},
#                         "aggs": {
#                             "mutations": {
#                                 "terms": {"field": "mutations.mutation", "size": 10000},
#                                 "aggs": {"genomes": {"reverse_nested": {}}},
#                             }
#                         },
#                     }
#                 },
#             }
#             query_lineage_split = query_lineage.split(" AND ")
#             query_mutations = []
#             query_pangolin_lineage = query_lineage_split[0].split(
#                 " OR "
#             )  # First parameter always lineages separated by commas
#             if len(query_lineage_split) > 1:
#                 query_mutations = query_lineage_split[1:]  # First parameter is always lineage
#             query["query"] = create_nested_mutation_query(
#                 lineages=query_pangolin_lineage, mutations=query_mutations
#             )

#             self.observability.log("es_query_before", query)

#             # print(query)
#             resp = await self.asynchronous_fetch(query)

#             self.observability.log("es_query_after", query)

#             path_to_results = ["aggregations", "mutations", "mutations", "buckets"]
#             buckets = resp
#             for i in path_to_results:
#                 buckets = buckets[i]
#             flattened_response = [
#                 {
#                     "mutation": i["key"],
#                     "mutation_count": i["genomes"]["doc_count"],
#                     "lineage_count": get_total_hits(resp),
#                     "lineage": query_lineage,
#                 }
#                 for i in buckets
#             ]
#             if len(flattened_response) > 0:
#                 df_response = pd.DataFrame(flattened_response).assign(
#                     gene=lambda x: x["mutation"].apply(
#                         lambda k: self.gene_mapping[k.split(":")[0]]
#                         if k.split(":")[0] in self.gene_mapping
#                         else k.split(":")[0]
#                     ),
#                     ref_aa=lambda x: x["mutation"]
#                     .apply(
#                         lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[0]
#                         if "DEL" not in k and "del" not in k and "_" not in k
#                         else k
#                     )
#                     .str.upper(),
#                     alt_aa=lambda x: x["mutation"]
#                     .apply(
#                         lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[1]
#                         if "DEL" not in k and "del" not in k and "_" not in k
#                         else k.split(":")[1]
#                     )
#                     .str.upper(),
#                     codon_num=lambda x: x["mutation"].apply(
#                         lambda k: int(re.findall("[0-9]+", k.split(":")[1])[0])
#                     ),
#                     codon_end=lambda x: x["mutation"].apply(
#                         lambda k: int(re.findall("[0-9]+", k.split(":")[1])[1])
#                         if "/" in k and ("DEL" in k or "del" in k)
#                         else None
#                     ),
#                     type=lambda x: x["mutation"].apply(
#                         lambda k: "deletion" if "DEL" in k or "del" in k else "substitution"
#                     ),
#                 )
#                 df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
#                 df_response.loc[:, "prevalence"] = (
#                     df_response["mutation_count"] / df_response["lineage_count"]
#                 )
#                 df_response.loc[~df_response["codon_end"].isna(), "change_length_nt"] = (
#                     (df_response["codon_end"] - df_response["codon_num"]) + 1
#                 ) * 3
#                 df_response = df_response[df_response["prevalence"] >= frequency].fillna("None")
#                 if genes:
#                     df_response = df_response[df_response["gene"].str.lower().isin(genes)]
#                 dict_response[query_lineage] = df_response.to_dict(orient="records")

#             # o.log("transformations")

#         self.observability.release_time()

#         tasks = [process_query(query_lineage) for query_lineage in pangolin_lineage.split(",")]
#         await asyncio.gather(*tasks)

#         resp = {"success": True, "results": dict_response}

#         self.observability.log("before_return")

#         return resp





# #######################
# ###### NORMAL

# import re
# import pandas as pd

# from web.handlers.genomics.base import BaseHandler
# from web.handlers.genomics.util import create_nested_mutation_query, get_total_hits


# class LineageMutationsHandler(BaseHandler):
#     gene_mapping = {
#         "orf1a": "ORF1a",
#         "orf1b": "ORF1b",
#         "s": "S",
#         "orf3a": "ORF3a",
#         "e": "E",
#         "m": "M",
#         "orf6": "ORF6",
#         "orf7a": "ORF7a",
#         "orf7b": "ORF7b",
#         "orf8": "ORF8",
#         "n": "N",
#         "orf10": "ORF10",
#     }

#     name = "lineage-mutations"
#     kwargs = dict(BaseHandler.kwargs)
#     kwargs["GET"] = {
#         "pangolin_lineage": {"type": str, "required": True},
#         "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
#         "gene": {"type": str, "default": None},
#     }

#     async def _get(self):
#         self.observability.log("function_get", self.args)
#         self.observability.lock_time()
#         pangolin_lineage = self.args.pangolin_lineage
#         frequency = self.args.frequency
#         gene = self.args.gene
#         if gene:
#             genes = gene.lower().split(",")
#         else:
#             genes = []
#         dict_response = {}
#         # Query structure: Lineage 1 OR Lineage 2 OR Lineage 3 AND Mutation 1 AND Mutation 2, Lineage 4 AND Mutation 2, Lineage 5 ....
#         for query_lineage in pangolin_lineage.split(","):
#             query = {
#                 "size": 0,
#                 "query": {},
#                 "aggs": {
#                     "mutations": {
#                         "nested": {"path": "mutations"},
#                         "aggs": {
#                             "mutations": {
#                                 "terms": {"field": "mutations.mutation", "size": 10000},
#                                 "aggs": {"genomes": {"reverse_nested": {}}},
#                             }
#                         },
#                     }
#                 },
#             }
#             query_lineage_split = query_lineage.split(" AND ")
#             query_mutations = []
#             query_pangolin_lineage = query_lineage_split[0].split(
#                 " OR "
#             )  # First parameter always lineages separated by commas
#             if len(query_lineage_split) > 1:
#                 query_mutations = query_lineage_split[1:]  # First parameter is always lineage
#             query["query"] = create_nested_mutation_query(
#                 lineages=query_pangolin_lineage, mutations=query_mutations
#             )

#             self.observability.log("es_query_before", query)

#             print("#######")
#             print(query)
#             resp = await self.asynchronous_fetch(query)

#             self.observability.log("es_query_after", query)

#             path_to_results = ["aggregations", "mutations", "mutations", "buckets"]
#             buckets = resp
#             for i in path_to_results:
#                 buckets = buckets[i]
#             flattened_response = [
#                 {
#                     "mutation": i["key"],
#                     "mutation_count": i["genomes"]["doc_count"],
#                     "lineage_count": get_total_hits(resp),
#                     "lineage": query_lineage,
#                 }
#                 for i in buckets
#             ]
#             if len(flattened_response) > 0:
#                 df_response = pd.DataFrame(flattened_response).assign(
#                     gene=lambda x: x["mutation"].apply(
#                         lambda k: self.gene_mapping[k.split(":")[0]]
#                         if k.split(":")[0] in self.gene_mapping
#                         else k.split(":")[0]
#                     ),
#                     ref_aa=lambda x: x["mutation"]
#                     .apply(
#                         lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[0]
#                         if "DEL" not in k and "del" not in k and "_" not in k
#                         else k
#                     )
#                     .str.upper(),
#                     alt_aa=lambda x: x["mutation"]
#                     .apply(
#                         lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[1]
#                         if "DEL" not in k and "del" not in k and "_" not in k
#                         else k.split(":")[1]
#                     )
#                     .str.upper(),
#                     codon_num=lambda x: x["mutation"].apply(
#                         lambda k: int(re.findall("[0-9]+", k.split(":")[1])[0])
#                     ),
#                     codon_end=lambda x: x["mutation"].apply(
#                         lambda k: int(re.findall("[0-9]+", k.split(":")[1])[1])
#                         if "/" in k and ("DEL" in k or "del" in k)
#                         else None
#                     ),
#                     type=lambda x: x["mutation"].apply(
#                         lambda k: "deletion" if "DEL" in k or "del" in k else "substitution"
#                     ),
#                 )
#                 df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
#                 df_response.loc[:, "prevalence"] = (
#                     df_response["mutation_count"] / df_response["lineage_count"]
#                 )
#                 df_response.loc[~df_response["codon_end"].isna(), "change_length_nt"] = (
#                     (df_response["codon_end"] - df_response["codon_num"]) + 1
#                 ) * 3
#                 df_response = df_response[df_response["prevalence"] >= frequency].fillna("None")
#                 if genes:
#                     df_response = df_response[df_response["gene"].str.lower().isin(genes)]
#                 dict_response[query_lineage] = df_response.to_dict(orient="records")

#             self.observability.log("transformations")

#         self.observability.release_time()

#         resp = {"success": True, "results": dict_response}

#         self.observability.log("before_return")

#         return resp









########################
####### ONE QUERY FIRST VERSION WORKING

# import re
# import observability
# import pandas as pd

# from web.handlers.genomics.base import BaseHandler
# from web.handlers.genomics.util import create_nested_mutation_query, get_total_hits


# class LineageMutationsHandler(BaseHandler):
#     gene_mapping = {
#         "orf1a": "ORF1a",
#         "orf1b": "ORF1b",
#         "s": "S",
#         "orf3a": "ORF3a",
#         "e": "E",
#         "m": "M",
#         "orf6": "ORF6",
#         "orf7a": "ORF7a",
#         "orf7b": "ORF7b",
#         "orf8": "ORF8",
#         "n": "N",
#         "orf10": "ORF10",
#     }

#     name = "lineage-mutations"
#     kwargs = dict(BaseHandler.kwargs)
#     kwargs["GET"] = {
#         "pangolin_lineage": {"type": str, "required": True},
#         "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
#         "gene": {"type": str, "default": None},
#     }

#     async def _get(self):
#         o = observability.Observability()
#         o.log("function_get", self.args)
#         o.lock_time()
#         pangolin_lineage = self.args.pangolin_lineage
#         frequency = self.args.frequency
#         gene = self.args.gene
#         if gene:
#             genes = gene.lower().split(",")
#         else:
#             genes = []
#         dict_response = {}


#         query = {
#             "size": 0,
#             "query": {
#                 "bool": {
#                     "should": []
#                 }
#             },
#             "aggs": {
#             "pangolin_lineage": {
#                 "terms": {
#                 "field": "pangolin_lineage",
#                 "size": 10000
#                 },
#                 "aggs": {
#                 "mutations": {
#                     "nested": {
#                     "path": "mutations"
#                     },
#                     "aggs": {
#                     "mutations": {
#                         "terms": {
#                         "field": "mutations.mutation",
#                         "size": 2
#                         },
#                         "aggs": {
#                         "genomes": {
#                             "reverse_nested": {}
#                         }
#                         }
#                     }
#                     }
#                 }
#                 }
#             }
#             }
#         }

#         for query_lineage in pangolin_lineage.split(","):
#             # print("#######")
#             # print(query_lineage)
#             # query["query"]["bool"]["should"].append({
#             #         "bool": {
#             #         "must": [
#             #             {
#             #             "term": {
#             #                 "pangolin_lineage": "AY.127.2"
#             #             }
#             #             }
#             #         ]
#             #         }
#             #     })
#             query_lineage_split = query_lineage.split(" AND ")
#             query_mutations = []
#             query_pangolin_lineage = query_lineage_split[0].split(
#                 " OR "
#             )  # First parameter always lineages separated by commas
#             if len(query_lineage_split) > 1:
#                 query_mutations = query_lineage_split[1:]  # First parameter is always lineage
#             query["query"]["bool"]["should"].append(create_nested_mutation_query(
#                 lineages=query_pangolin_lineage, mutations=query_mutations
#             )["bool"]["should"][0])

#         o.log("es_query_before", query)

#         print("#########")
#         print(query)

#         resp = await self.asynchronous_fetch(query)

#         o.log("es_query_after", query)

#         print("!!!!!!!!!!!!!!")
#         print(str(resp))

#         # path_to_pangolin_lineage_buckets_results = ["aggregations", "pangolin_lineage", "buckets"]
#         # pangolin_lineage_buckets = resp
#         # for pangolin_lineage_bucket in path_to_pangolin_lineage_buckets_results:
#         #     pangolin_lineage_buckets = pangolin_lineage_buckets[pangolin_lineage_bucket]

#         for pangolin_lineage_bucket in resp["aggregations"]["pangolin_lineage"]["buckets"]:
#             # print("@@@@@@")
#             # print(pangolin_lineage_bucket["key"])

#             # path_to_results = ["aggregations", "mutations", "mutations", "buckets"]
#             path_to_results = ["mutations", "mutations", "buckets"]
#             buckets = pangolin_lineage_bucket
#             for i in path_to_results:
#                 buckets = buckets[i]
#                 print("$$$$$$$")
#                 print(buckets)

#             query_lineage = pangolin_lineage_bucket["key"]

#             flattened_response = [
#                 {
#                     "mutation": i["key"],
#                     "mutation_count": i["genomes"]["doc_count"],
#                     "lineage_count": get_total_hits(resp),
#                     "lineage": query_lineage,
#                 }
#                 for i in buckets
#             ]
#             if len(flattened_response) > 0:
#                 df_response = pd.DataFrame(flattened_response).assign(
#                     gene=lambda x: x["mutation"].apply(
#                         lambda k: self.gene_mapping[k.split(":")[0]]
#                         if k.split(":")[0] in self.gene_mapping
#                         else k.split(":")[0]
#                     ),
#                     ref_aa=lambda x: x["mutation"]
#                     .apply(
#                         lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[0]
#                         if "DEL" not in k and "del" not in k and "_" not in k
#                         else k
#                     )
#                     .str.upper(),
#                     alt_aa=lambda x: x["mutation"]
#                     .apply(
#                         lambda k: re.findall("[A-Za-z*]+", k.split(":")[1])[1]
#                         if "DEL" not in k and "del" not in k and "_" not in k
#                         else k.split(":")[1]
#                     )
#                     .str.upper(),
#                     codon_num=lambda x: x["mutation"].apply(
#                         lambda k: int(re.findall("[0-9]+", k.split(":")[1])[0])
#                     ),
#                     codon_end=lambda x: x["mutation"].apply(
#                         lambda k: int(re.findall("[0-9]+", k.split(":")[1])[1])
#                         if "/" in k and ("DEL" in k or "del" in k)
#                         else None
#                     ),
#                     type=lambda x: x["mutation"].apply(
#                         lambda k: "deletion" if "DEL" in k or "del" in k else "substitution"
#                     ),
#                 )
#                 df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
#                 df_response.loc[:, "prevalence"] = (
#                     df_response["mutation_count"] / df_response["lineage_count"]
#                 )
#                 df_response.loc[~df_response["codon_end"].isna(), "change_length_nt"] = (
#                     (df_response["codon_end"] - df_response["codon_num"]) + 1
#                 ) * 3
#                 df_response = df_response[df_response["prevalence"] >= frequency].fillna("None")
#                 if genes:
#                     df_response = df_response[df_response["gene"].str.lower().isin(genes)]
#                 dict_response[query_lineage] = df_response.to_dict(orient="records")

#             o.log("transformations")

#         o.release_time()

#         resp = {"success": True, "results": dict_response}

#         o.log("before_return")

#         return resp





########################
####### ONE QUERY SECOND VERSION

import re
import pandas as pd
import util

from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import create_nested_mutation_query, get_total_hits, lineage_mutation_aggregations


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
        self.observability.log("function_get", self.args)
        self.observability.lock_time()
        pangolin_lineages = self.args.pangolin_lineage
        frequency = self.args.frequency
        gene = self.args.gene
        if gene:
            genes = gene.lower().split(",")
        else:
            genes = []
        dict_response = {}

        query = {
            "size": 0,
            "query": {
                "terms": {
                    # Ex: "pangolin_lineage": ["AY.1", "B.1.617.2"]
                    "pangolin_lineage": list(set(pangolin_lineages.replace(" AND ",",").replace(" OR ",",").split(",")))
                }
            },
            "aggs": {
                **lineage_mutation_aggregations(pangolin_lineages)
            }
        }

        self.observability.log("es_query_before", query)

        resp = await self.asynchronous_fetch(query)

        self.observability.log("es_query_after", query)

        ### AND and OR aggregations 
        for key, pangolin_lineage_bucket in resp["aggregations"].items():
            if key != "pangolin_lineage_individual":
                # print("@@@@@@111111")
                # # print(pangolin_lineage_bucket)
                # print(key)
                # print(pangolin_lineage_bucket)

                path_to_results = ["mutations", "mutations", "buckets"]

                buckets = pangolin_lineage_bucket
                for i in path_to_results:
                    if i in buckets:
                        buckets = buckets[i]

                if isinstance(buckets, list):
                    query_lineage = key #pangolin_lineage_bucket["key"]

                    flattened_response = [
                        {
                            "mutation": i["key"],
                            "mutation_count": i["genomes"]["doc_count"],
                            "lineage_count": get_total_hits(resp),
                            "lineage": query_lineage,
                        }
                        for i in buckets
                    ]
                    # print("!!!!!!!")
                    # print(flattened_response)
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

                        # print("11")
                        # print(df_response.to_dict(orient="records"))

                        df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
                        df_response.loc[:, "prevalence"] = (
                            df_response["mutation_count"] / df_response["lineage_count"]
                        )

                        # print("22")
                        # print(df_response.to_dict(orient="records"))

                        df_response.loc[~df_response["codon_end"].isna(), "change_length_nt"] = (
                            (df_response["codon_end"] - df_response["codon_num"]) + 1
                        ) * 3

                        # print("33")
                        # print(df_response.to_dict(orient="records"))

                        df_response = df_response[df_response["prevalence"] >= frequency].fillna("None")

                        # print("44")
                        # print(df_response.to_dict(orient="records"))

                        if genes:
                            df_response = df_response[df_response["gene"].str.lower().isin(genes)]

                        # print("55")
                        # print(df_response.to_dict(orient="records"))

                        dict_response[query_lineage] = df_response.to_dict(orient="records")

                    self.observability.log("transformations")


        #######################################################
        #######################################################
        #######################################################

        ### Individual
        if "pangolin_lineage_individual" in resp["aggregations"]:
            for pangolin_lineage_bucket in resp["aggregations"]["pangolin_lineage_individual"]["pangolin_lineage"]["buckets"]:
                # print("@@@@@@")
                # # print(pangolin_lineage_bucket)
                # print(pangolin_lineage_bucket["key"])

                # path_to_results = ["aggregations", "mutations", "mutations", "buckets"]
                path_to_results = ["mutations", "mutations", "buckets"]
                buckets = pangolin_lineage_bucket
                for i in path_to_results:
                    buckets = buckets[i]
                    # print("$$$$$$$")
                    # print(buckets)

                query_lineage = pangolin_lineage_bucket["key"]

                flattened_response = [
                    {
                        "mutation": i["key"],
                        "mutation_count": i["genomes"]["doc_count"],
                        "lineage_count": get_total_hits(resp),
                        "lineage": query_lineage,
                    }
                    for i in buckets
                ]
                # print("!!!!!!!")
                # print(flattened_response)
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

                    # print("11")
                    # print(df_response.to_dict(orient="records"))

                    df_response = df_response[df_response["ref_aa"] != df_response["alt_aa"]]
                    df_response.loc[:, "prevalence"] = (
                        df_response["mutation_count"] / df_response["lineage_count"]
                    )

                    # print("22")
                    # print(df_response.to_dict(orient="records"))

                    df_response.loc[~df_response["codon_end"].isna(), "change_length_nt"] = (
                        (df_response["codon_end"] - df_response["codon_num"]) + 1
                    ) * 3

                    # print("33")
                    # print(df_response.to_dict(orient="records"))

                    df_response = df_response[df_response["prevalence"] >= frequency].fillna("None")

                    # print("44")
                    # print(df_response.to_dict(orient="records"))

                    if genes:
                        df_response = df_response[df_response["gene"].str.lower().isin(genes)]

                    # print("55")
                    # print(df_response.to_dict(orient="records"))

                    dict_response[query_lineage] = df_response.to_dict(orient="records")

                self.observability.log("transformations")

        self.observability.release_time()

        resp = {"success": True, "results": dict_response}

        self.observability.log("before_return")

        return resp
