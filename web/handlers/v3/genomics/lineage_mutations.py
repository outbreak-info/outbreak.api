import asyncio

import web.handlers.v3.genomics.adapters_in.lineage_mutations as adapters_in
import web.handlers.v3.genomics.adapters_out.lineage_mutations as adapters_out
import web.handlers.v3.genomics.es.lineage_mutations as es
from web.handlers.v3.genomics.base import BaseHandlerV3
from web.handlers.v3.genomics.util import create_iterator_q


class LineageMutationsHandler(BaseHandlerV3):
    name = "lineage-mutations-v3"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "q": {"type": str, "default": None},
        "pangolin_lineage": {"type": str},
        "lineages": {"type": str},
        "mutations": {"type": str},
        "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
        "gene": {"type": str, "default": None},
    }

    async def _get(self):
        params = adapters_in.params_adapter(self.args)

        parsed_resp = {}
        if (params["lineages"] is not None and params["lineages"] != "") or (
            params["mutations"] is not None and params["mutations"] != ""
        ):
            query = es.create_query(lineages=params["lineages"], mutations=params["mutations"])
            resp = await self.asynchronous_fetch_lineages(query=query)
            parsed_resp = adapters_out.parse_response(
                resp=resp,
                frequency=params["frequency"],
                lineages=params["lineages"],
                genes=params["genes"],
            )

        if "q" in params and params["q"] is not None:

            async def process_query_q(idx, query_filter):
                query = es.create_query_q(query_filter, self.size)
                query_resp = await self.asynchronous_fetch_lineages(query)
                parsed_resp.update(adapters_out.parse_response_q(resp=query_resp, idx=idx, params=params))

            tasks = [
                process_query_q(idx, query_filter)
                for idx, query_filter in create_iterator_q(params["query_string_list"])
            ]
            await asyncio.gather(*tasks)

        result = {"success": True, "results": parsed_resp}
        return result
