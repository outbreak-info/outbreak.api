import web.handlers.v3.genomics.helpers.lineage_helper as helper

from web.handlers.v3.genomics.base import BaseHandlerV3


class LineageHandler(BaseHandlerV3):
    name = "lineage"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "name": {"type": str, "default": None},
        "size": {"type": int, "default": None},
    }

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(resp=query_resp, size=params["size"])
        resp = {"success": True, "results": parsed_resp}
        return resp
