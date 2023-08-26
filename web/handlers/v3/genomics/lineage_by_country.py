import web.handlers.v3.genomics.helpers.lineage_by_country_helper as helper

from tornado import gen
from web.handlers.v3.genomics.base import BaseHandlerV3
from web.handlers.v3.genomics.util import (
    create_nested_mutation_query,
)

class LineageByCountryHandler(BaseHandlerV3):

    @gen.coroutine
    def _get(self):
        query_pangolin_lineage = self.get_argument("pangolin_lineage", None)
        query_mutations = self.get_argument("mutations", None)
        query = {
            "aggs": {
                "prevalence": {
                    "filter" : {},
                    "aggs": {
                        "country": {
                            "terms": {
                                "field": "country",
                                "size": self.size
                            }
                        }
                    }
                }
            }
        }
        # query_mutations = query_mutations.split(",") if query_mutations is not None else []
        # query_pangolin_lineage = query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
        lineages = query_pangolin_lineage if query_pangolin_lineage else ""
        mutations = query_mutations if query_mutations else ""

        query_obj = create_nested_mutation_query(lineages = lineages, mutations = mutations)
        query["aggs"]["prevalence"]["filter"] = query_obj
        # self.observability.log("es_query_before", query)
        resp = yield self.asynchronous_fetch(query)
        # self.observability.log(resp, "es_response")
        parsed_resp = helper.parse_response(resp)
        # self.observability.log(parsed_resp, "parsed_response")
        result = {"success": True, "results": parsed_resp}
        # self.observability.log(result, "result")
        return result
