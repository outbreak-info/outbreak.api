import asyncio

import web.handlers.v3.genomics.adapters_in.prevalence_by_location as adapters_in
import web.handlers.v3.genomics.adapters_out.prevalence_by_location as adapters_out
import web.handlers.v3.genomics.es.prevalence_by_location as es
from web.handlers.v3.genomics.base import BaseHandlerV3
from web.handlers.v3.genomics.util import create_iterator, create_iterator_q


class PrevalenceByLocationAndTimeHandler(BaseHandlerV3):
    name = "prevalence-by-location"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "q": {"type": str, "default": None},
        "pangolin_lineage": {"type": str, "default": None},
        "mutations": {"type": str, "default": None},
        "location_id": {"type": str, "default": None},
        "cumulative": {"type": bool, "default": False},
        "min_date": {"type": str, "default": None, "date_format": "%Y-%m-%d"},
        "max_date": {"type": str, "default": None, "date_format": "%Y-%m-%d"},
    }

    async def _get(self):
        params = adapters_in.params_adapter(self.args)
        parsed_resp = {}

        async def process_query(idx, i, j):
            query = es.create_query(idx, params, self.size)
            query_resp = await self.asynchronous_fetch_lineages(query)
            parsed_resp.update(adapters_out.parse_response(resp=query_resp, idx=idx, params=params))
            idx = idx + 1

        tasks = [
            process_query(idx, i, j)
            for idx, i, j in create_iterator(params["pangolin_lineage"], params["mutations"])
        ]
        await asyncio.gather(*tasks)

        if "q" in params and params["q"] is not None:

            async def process_query_q(idx, i):
                query = es.create_query_q(idx, params, self.size)
                query_resp = await self.asynchronous_fetch_lineages(query)
                parsed_resp.update(
                    adapters_out.parse_response_q(resp=query_resp, idx=idx, params=params)
                )

            tasks = [process_query_q(idx, i) for idx, i in create_iterator_q(params["q_list"])]
            await asyncio.gather(*tasks)

        resp = {"success": True, "results": parsed_resp}
        return resp
