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
        resp = await self.asynchronous_fetch(query)
        dict_response = helper.parse_response(resp=resp, size=params["size"])
        resp = {"success": True, "results": dict_response}
        return resp
