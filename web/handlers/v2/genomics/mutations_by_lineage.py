import pandas as pd

from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import (
    calculate_proportion,
    create_nested_mutation_query,
    parse_location_id_to_query,
)


class MutationsByLineage(BaseHandler):
    name = "mutations-by-lineage"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "location_id": {"type": str, "default": None},
        "mutations": {"type": str, "default": None},
        "pangolin_lineage": {"type": str, "default": None},
        "frequency": {"type": float, "default": 0, "min": 0, "max": 1},
    }

    async def _get(self):
        query_location = self.args.location_id
        query_mutations = self.args.mutations
        query_pangolin_lineage = self.args.pangolin_lineage
        query_mutations = (
            [muts.split(",") for muts in query_mutations.split(" AND ")]
            if query_mutations is not None
            else []
        )
        query_frequency_threshold = self.args.frequency
        results = {}
        for (
            muts
        ) in (
            query_mutations
        ):  # For multiple sets of mutations, create multiple ES queries. Since AND queries are possible doing one ES query with aggregations is cumbersome. Must look for better solution here.
            query = {
                "size": 0,
                "aggs": {
                    "lineage": {
                        "terms": {"field": "pangolin_lineage", "size": self.size},
                        "aggs": {"mutations": {"filter": {}}},
                    }
                },
            }
            if query_location is not None:
                query["query"] = parse_location_id_to_query(query_location)
            if query_pangolin_lineage is not None:
                if "query" in query:  # Only query added will be bool for location
                    query["query"]["bool"]["must"].append(
                        {"term": {"pangolin_lineage": query_pangolin_lineage}}
                    )
                else:
                    query["query"] = {"term": {"pangolin_lineage": query_pangolin_lineage}}
            query["aggs"]["lineage"]["aggs"]["mutations"]["filter"] = create_nested_mutation_query(
                mutations=muts
            )
            resp = await self.asynchronous_fetch(query)
            path_to_results = ["aggregations", "lineage", "buckets"]
            buckets = resp
            for i in path_to_results:
                buckets = buckets[i]
            flattened_response = []
            for i in buckets:
                if not i["mutations"]["doc_count"] > 0 or i["key"] == "none":
                    continue
                flattened_response.append(
                    {
                        "pangolin_lineage": i["key"],
                        "lineage_count": i["doc_count"],
                        "mutation_count": i["mutations"]["doc_count"],
                    }
                )
            df_response = pd.DataFrame(flattened_response)
            if df_response.shape[0] > 0:
                prop = calculate_proportion(
                    df_response["mutation_count"], df_response["lineage_count"]
                )
                df_response.loc[:, "proportion"] = prop[0]
                df_response.loc[:, "proportion_ci_lower"] = prop[1]
                df_response.loc[:, "proportion_ci_upper"] = prop[2]
            df_response = df_response[df_response["proportion"] >= query_frequency_threshold]
            results[",".join(muts)] = df_response.to_dict(orient="records")
        resp = {"success": True, "results": results}
        return resp
