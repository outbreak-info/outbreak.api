import pandas as pd
import web.handlers.v3.genomics.helpers.lineage_helper as helper

from tornado import gen
from web.handlers.v3.genomics.base import BaseHandlerV3
from web.handlers.v3.genomics.util import (
    create_nested_mutation_query,
    calculate_proportion,
    parse_location_id_to_query
)


class LineageHandler(BaseHandlerV3):
    name = "lineage"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "name": {"type": str, "default": None},
        "size": {"type": int, "default": None},
    }

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(resp=query_resp, size=params["size"])
        resp = {"success": True, "results": parsed_resp}
        return resp

class MutationsByLineage(BaseHandlerV3):
    @gen.coroutine
    def _get(self):
        query_location = self.get_argument("location_id", None)
        query_mutations = self.get_argument("mutations", None)
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_mutations = [muts for muts in query_mutations.split(" AND ")] if query_mutations is not None else []
        query_frequency_threshold = self.get_argument("frequency", None)
        query_frequency_threshold = float(query_frequency_threshold) if query_frequency_threshold is not None else 0
        results = {}

        for muts in query_mutations: # For multiple sets of mutations, create multiple ES queries. Since AND queries are possible doing one ES query with aggregations is cumbersome. Must look for better solution here.
            query = {
                "size": 0,
                "aggs": {
                "lineage": {
                        "terms": {"field": "pangolin_lineage", "size": self.size},
                        "aggs": {
                            "mutations": {
                                "filter": {}
                            }
                        }
                    }
                }
            }
            if query_location is not None:
                query["query"] = parse_location_id_to_query(query_location)
            if query_pangolin_lineage is not None:
                if "query" in query: # Only query added will be bool for location
                    query["query"]["bool"]["must"].append({
                        "term": {
                            "pangolin_lineage": query_pangolin_lineage
                        }
                    })
                else:
                    query["query"] = {
                        "term": {
                            "pangolin_lineage": query_pangolin_lineage
                        }
                    }
            query["aggs"]["lineage"]["aggs"]["mutations"]["filter"] = create_nested_mutation_query(mutations = muts)
            resp = yield self.asynchronous_fetch(query)
            path_to_results = ["aggregations", "lineage", "buckets"]
            buckets = resp
            for i in path_to_results:
                buckets = buckets[i]
            flattened_response = []
            for i in buckets:
                if not i["mutations"]["doc_count"] > 0 or i["key"] == "none":
                    continue
                flattened_response.append({
                    "pangolin_lineage": i["key"],
                    "lineage_count": i["doc_count"],
                    "mutation_count": i["mutations"]["doc_count"]
                })
            df_response = pd.DataFrame(flattened_response)
            if df_response.shape[0] > 0:
                prop = calculate_proportion(df_response["mutation_count"], df_response["lineage_count"])
                df_response.loc[:, "proportion"] = prop[0]
                df_response.loc[:, "proportion_ci_lower"] = prop[1]
                df_response.loc[:, "proportion_ci_upper"] = prop[2]
            df_response = df_response[df_response["proportion"] >= query_frequency_threshold]
            results[muts] = df_response.to_dict(orient="records")

        resp = {"success": True, "results": results}
        return resp
