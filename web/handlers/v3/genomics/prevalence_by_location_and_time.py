import asyncio

import web.handlers.v3.genomics.helpers.prevalence_by_location_helper as helper
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
        params = helper.params_adapter(self.args)
        parsed_resp = {}

        async def process_query(idx, i, j):
            query = helper.create_query(idx, params, self.size)
            query_resp = await self.asynchronous_fetch(query)
            parsed_resp.update(helper.parse_response(resp=query_resp, idx=idx, params=params))
            idx = idx + 1

        tasks = [
            process_query(idx, i, j)
            for idx, i, j in create_iterator(params["pangolin_lineage"], params["mutations"])
        ]
        await asyncio.gather(*tasks)

        if "q" in params and params["q"] is not None:

            async def process_query_q(idx, i):
                query = helper.create_query_q(idx, params, self.size)
                query_resp = await self.asynchronous_fetch(query)
                parsed_resp.update(helper.parse_response_q(resp=query_resp, idx=idx, params=params))

            tasks = [process_query_q(idx, i) for idx, i in create_iterator_q(params["q_list"])]
            await asyncio.gather(*tasks)

        resp = {"success": True, "results": parsed_resp}
        return resp
