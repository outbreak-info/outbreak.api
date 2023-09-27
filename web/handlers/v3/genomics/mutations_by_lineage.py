import asyncio

import web.handlers.v3.genomics.adapters_in.mutations_by_lineage as adapters_in
import web.handlers.v3.genomics.adapters_out.mutations_by_lineage as adapters_out
import web.handlers.v3.genomics.es.mutations_by_lineage as es
from web.handlers.v3.genomics.base import BaseHandlerV3
from web.handlers.v3.genomics.util import create_iterator_q


class MutationsByLineage(BaseHandlerV3):
    name = "mutations-by-lineage"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "q": {"type": str, "default": None},
        "pangolin_lineage": {"type": str},
        "mutations": {"type": str, "default": None},
        "location_id": {"type": str, "default": None},
        "frequency": {"type": float, "default": 0, "min": 0, "max": 1},
    }

    async def _get(self):
        params = adapters_in.params_adapter(self.args)
        parsed_resp = {}

        if params["mutations"] is not None and params["mutations"] != "":

            async def process_query(mutation):
                query = es.create_query(mutation, params, self.size)
                query_resp = await self.asynchronous_fetch_lineages(query)
                parsed_resp.update(
                    adapters_out.parse_response(resp=query_resp, mutation=mutation, params=params)
                )

            tasks = [process_query(mutation) for mutation in params["mutations_list"]]
            await asyncio.gather(*tasks)

        if "q" in params and params["q"] is not None:

            async def process_query_q(idx, query_filter):
                query = es.create_query_q(query_filter, params, self.size)
                query_resp = await self.asynchronous_fetch_lineages(query)
                parsed_resp.update(
                    adapters_out.parse_response_q(resp=query_resp, idx=idx, params=params)
                )

            tasks = [
                process_query_q(idx, query_filter)
                for idx, query_filter in create_iterator_q(params["query_string_list"])
            ]
            await asyncio.gather(*tasks)

        resp = {"success": True, "results": parsed_resp}
        return resp
