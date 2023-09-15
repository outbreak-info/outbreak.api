import web.handlers.v3.genomics.helpers.prevalence_helper as helper
from web.handlers.v3.genomics.base import BaseHandlerV3

from .util import transform_prevalence


# Get global prevalence of lineage by date
class GlobalPrevalenceByTimeHandler(BaseHandlerV3):
    name = "global-prevalence-by-time"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str, "required": False},
        "mutations": {"type": str, "required": False},
        "cumulative": {"type": bool, "required": False},
    }

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params, self.size)
        query_resp = await self.asynchronous_fetch_lineages(query)
        path_to_results = ["aggregations", "prevalence", "buckets"]
        resp = transform_prevalence(query_resp, path_to_results, params["cumulative"])
        resp = {"success": True, "results": resp}
        return resp
