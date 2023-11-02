import web.handlers.v3.genomics.adapters_in.lineage_by_country as adapters_in
import web.handlers.v3.genomics.adapters_out.lineage_by_country as adapters_out
import web.handlers.v3.genomics.es.lineage_by_country as es
from web.handlers.v3.genomics.base import BaseHandlerV3


class LineageByCountryHandler(BaseHandlerV3):
    name = "lineage-by-country"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str, "default": None},
        "mutations": {"type": str, "default": None},
    }

    async def _get(self):
        params = adapters_in.params_adapter(self.args)
        query = es.create_query(params, self.size)
        query_resp = await self.asynchronous_fetch_lineages(query)
        parsed_resp = adapters_out.parse_response(query_resp)
        resp = {"success": True, "results": parsed_resp}
        return resp
