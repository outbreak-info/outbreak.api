import web.handlers.v3.genomics.helpers.lineage_by_country_helper as helper

from web.handlers.v3.genomics.base import BaseHandlerV3


class LineageByCountryHandler(BaseHandlerV3):
    name = "lineage-by-country"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str, "default": None},
        "mutations": {"type": str, "default": None},
    }

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params, self.size)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(query_resp)
        resp = {"success": True, "results": parsed_resp}
        return resp
