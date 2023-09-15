import web.handlers.v3.genomics.helpers.sequence_count_helper as helper
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
        params = helper.params_adapter(self.args)
        query = helper.create_query(params, self.size)
        query_resp = await self.asynchronous_fetch_lineages(query)
        parsed_resp = helper.parse_response(query_resp, params)
        resp = {"success": True, "results": parsed_resp}
        return resp
