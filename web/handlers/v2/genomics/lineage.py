import web.handlers.v2.genomics.helpers.lineage_helper as helper

from web.handlers.genomics.base import BaseHandler


class LineageHandler(BaseHandler):

    kwargs = dict(BaseHandler.kwargs)
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
