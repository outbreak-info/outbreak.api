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
                                "field": "country.keyword",
                                "size": self.size
                            }
                        }
                    }
                }
            }
        }
        query_mutations = query_mutations.split(",") if query_mutations is not None else []
        query_pangolin_lineage = query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
        query_obj = create_nested_mutation_query(lineages = query_pangolin_lineage, mutations = query_mutations)
        query["aggs"]["prevalence"]["filter"] = query_obj
        resp = yield self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(resp)
        result = {"success": True, "results": parsed_resp}
        return result
