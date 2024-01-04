import web.handlers.v3.genomics.adapters_in.mutation_details as adapters_in
import web.handlers.v3.genomics.adapters_out.mutation_details as adapters_out
import web.handlers.v3.genomics.es.mutation_details as es
from web.handlers.v3.genomics.base import BaseHandlerV3


class MutationDetailsHandler(BaseHandlerV3):
    name = "mutation-details"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {"mutations": {"type": str, "default": None}}

    async def _get(self):
        params = adapters_in.params_adapter(self.args)
        query = es.create_query(params)
        query_resp = await self.asynchronous_fetch_mutations(query)
        parsed_resp = adapters_out.parse_response(resp=query_resp)
        resp = {"success": True, "results": parsed_resp}
        return resp
