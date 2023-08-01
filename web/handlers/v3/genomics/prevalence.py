from .util import (
    transform_prevalence,
    create_nested_mutation_query
)
from web.handlers.v3.genomics.base import BaseHandlerV3
from tornado import gen

# Get global prevalence of lineage by date
class GlobalPrevalenceByTimeHandler(BaseHandlerV3):

    @gen.coroutine
    def _get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_mutations = self.get_argument("mutations", None)
        cumulative = self.get_argument("cumulative", None)
        cumulative = True if cumulative == "true" else False
        query = {
            "size": 0,
            "aggs": {
                "prevalence": {
                    "terms": {
                        "field": "date_collected",
                        "size": self.size
                    },
                    "aggs": {
                        "lineage_count": {
                            "filter": {}
                        }
                    }
                }
            }
        }
        query_obj = create_nested_mutation_query(lineages = query_pangolin_lineage, mutations = query_mutations)
        query["aggs"]["prevalence"]["aggs"]["lineage_count"]["filter"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "prevalence", "buckets"]
        resp = transform_prevalence(resp, path_to_results, cumulative)
        return {
            "success": True,
            "results": resp
        }
