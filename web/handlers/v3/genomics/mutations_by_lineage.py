import asyncio

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
        parsed_resp = {}

        if (params["mutations"] is not None and params["mutations"] != ""):
            async def process_query(mutation):
                query = helper.create_query(mutation, params, self.size)
                self.observability.log(query)
                query_resp = await self.asynchronous_fetch_lineages(query)
                parsed_resp.update(
                    helper.parse_response(resp=query_resp, mutation=mutation, params=params)
                )

            tasks = [process_query(mutation) for mutation in params["mutations_list"]]
            await asyncio.gather(*tasks)

        resp = {"success": True, "results": parsed_resp}
        return resp
