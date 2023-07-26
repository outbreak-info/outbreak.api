import web.handlers.v2.genomics.helpers.mutation_details_helper as helper

from web.handlers.genomics.base import BaseHandler


class MutationDetailsHandler(BaseHandler):
    name = "mutation-details"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {"mutations": {"type": str, "default": None}}

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(resp=query_resp)
        resp = {"success": True, "results": parsed_resp}
        return resp
