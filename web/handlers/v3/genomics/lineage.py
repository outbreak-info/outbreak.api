import web.handlers.v3.genomics.adapters_in.lineage as adapters_in
import web.handlers.v3.genomics.adapters_out.lineage as adapters_out
import web.handlers.v3.genomics.es.lineage as es
from web.handlers.v3.genomics.base import BaseHandlerV3


class LineageHandler(BaseHandlerV3):
    name = "lineage"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "name": {"type": str, "default": None},
        "size": {"type": int, "default": None},
    }

    async def _get(self):
        params = adapters_in.params_adapter(self.args)
        query = es.create_query(params)
        query_resp = await self.asynchronous_fetch_lineages(query)
        parsed_resp = adapters_out.parse_response(resp=query_resp, size=params["size"])
        resp = {"success": True, "results": parsed_resp}
        return resp
