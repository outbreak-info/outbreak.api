import web.handlers.v3.genomics.helpers.mutation_details_helper as helper
from web.handlers.v3.genomics.base import BaseHandlerV3


class MutationDetailsHandler(BaseHandlerV3):
    name = "mutation-details"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {"mutations": {"type": str, "default": None}}

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(resp=query_resp)
        resp = {"success": True, "results": parsed_resp}
        return resp
