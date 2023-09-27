from typing import Dict

from web.handlers.v3.genomics.util import transform_prevalence


def parse_response(query_resp: Dict = None, params: Dict = None) -> Dict:
    path_to_results = ["aggregations", "prevalence", "buckets"]
    return transform_prevalence(query_resp, path_to_results, params["cumulative"])
