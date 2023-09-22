import web.handlers.v3.genomics.adapters_in.mutations as adapters_in
import web.handlers.v3.genomics.adapters_out.mutations as adapters_out
import web.handlers.v3.genomics.es.mutations as es
from web.handlers.v3.genomics.base import BaseHandlerV3


class MutationHandler(BaseHandlerV3):
    name = "mutations"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "name": {"type": str, "required": True},
    }

    async def _get(self):
        params = adapters_in.params_adapter(self.args)
        query = es.create_query(params)
        query_resp = await self.asynchronous_fetch_mutations(query)
        parsed_resp = adapters_out.parse_response(resp=query_resp)
        resp = {"success": True, "results": parsed_resp}
        return resp
