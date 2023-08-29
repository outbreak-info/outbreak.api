import web.handlers.v3.genomics.helpers.mutations_by_lineage_helper as helper

from web.handlers.v3.genomics.base import BaseHandlerV3


class MutationsByLineage(BaseHandlerV3):
    name = "mutations-by-lineage"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str},
        "mutations": {"type": str, "default": None},
        "location_id": {"type": str, "default": None},
        "frequency": {"type": float, "default": 0, "min": 0, "max": 1},
    }

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params, self.size)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(resp=query_resp, params=params)
        resp = {"success": True, "results": parsed_resp}
        return resp
