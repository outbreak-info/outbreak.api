import web.handlers.v3.genomics.adapters_in.sequence_count as adapter_in
import web.handlers.v3.genomics.adapters_out.sequence_count as adapter_out
import web.handlers.v3.genomics.es.sequence_count as es
from web.handlers.v3.genomics.base import BaseHandlerV3


class SequenceCountHandler(BaseHandlerV3):
    name = "sequence-count"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "location_id": {"type": str, "default": None},
        "cumulative": {"type": bool, "default": False},
        "subadmin": {"type": bool, "default": False},
    }

    async def _get(self):
        params = adapter_in.params_adapter(self.args)
        query = es.create_query(params, self.size)
        query_resp = await self.asynchronous_fetch_lineages(query)
        parsed_resp = adapter_out.parse_response(query_resp, params)
        resp = {"success": True, "results": parsed_resp}
        return resp
