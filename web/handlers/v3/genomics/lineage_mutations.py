import asyncio

import web.handlers.v3.genomics.helpers.lineage_mutations_helper as helper
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
        params = helper.params_adapter(self.args)

        parsed_resp = {}
        if (params["lineages"] is not None and params["lineages"] != "") or (
            params["mutations"] is not None and params["mutations"] != ""
        ):
            query = helper.create_query(lineages=params["lineages"], mutations=params["mutations"])
            resp = await self.asynchronous_fetch_lineages(query=query)
            parsed_resp = helper.parse_response(
                resp=resp,
                frequency=params["frequency"],
                lineages=params["lineages"],
                genes=params["genes"],
            )

        if "q" in params and params["q"] is not None:

            async def process_query_q(idx, query_filter):
                query = helper.create_query_q(query_filter, self.size)
                self.observability.log("ES_QUERY", query)
                query_resp = await self.asynchronous_fetch_lineages(query)
                # self.observability.log("ES_RESPONSE", query_resp)
                parsed_resp.update(helper.parse_response_q(resp=query_resp, idx=idx, params=params))

            tasks = [
                process_query_q(idx, query_filter)
                for idx, query_filter in create_iterator_q(params["query_string_list"])
            ]
            await asyncio.gather(*tasks)

        result = {"success": True, "results": parsed_resp}
        return result
