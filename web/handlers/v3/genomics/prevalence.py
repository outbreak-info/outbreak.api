import web.handlers.v3.genomics.adapters_in.prevalence as adapters_in
import web.handlers.v3.genomics.adapters_out.prevalence as adapters_out
import web.handlers.v3.genomics.es.prevalence as es
from web.handlers.v3.genomics.base import BaseHandlerV3


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
        params = adapters_in.params_adapter(self.args)
        query = es.create_query(params, self.size)
        query_resp = await self.asynchronous_fetch_lineages(query)
        resp = adapters_out.parse_response(query_resp=query_resp, params=params)
        resp = {"success": True, "results": resp}
        return resp
