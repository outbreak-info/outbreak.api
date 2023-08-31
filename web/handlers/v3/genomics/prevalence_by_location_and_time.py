import asyncio
import web.handlers.v3.genomics.helpers.prevalence_by_location_helper as helper

from web.handlers.v3.genomics.base import BaseHandlerV3
from web.handlers.v3.genomics.util import (
    create_iterator,
)


class PrevalenceByLocationAndTimeHandler(BaseHandlerV3):
    name = "prevalence-by-location"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str},
        "mutations": {"type": str, "default": None},
        "location_id": {"type": str, "default": None},
        "cumulative": {"type": bool, "default": False},
        "min_date": {"type": str, "default": None, "date_format": "%Y-%m-%d"},
        "max_date": {"type": str, "default": None, "date_format": "%Y-%m-%d"},
    }

    # async def _get(self):
    #     params = helper.params_adapter(self.args)
    #     query = helper.create_query(params, self.size)
    #     query_resp = await self.asynchronous_fetch(query)
    #     parsed_resp = helper.parse_response(query_resp, params)
    #     resp = {"success": True, "results": parsed_resp}
    #     return resp

    # async def _get(self):
    #     params = helper.params_adapter(self.args)
    #     parsed_resp = {}
        # idx = 0
        # for i, j in create_iterator(params["pangolin_lineage"], params["mutations"]):
        #     print("@@@ i")
        #     print(i)
        #     print("@@@ j")
        #     print(j)
        #     query = helper.create_query(idx, params, self.size)
        #     query_resp = await self.asynchronous_fetch(query)
        #     parsed_resp.update(helper.parse_response(query_resp, idx, params))
        #     idx = idx + 1
    #     resp = {"success": True, "results": parsed_resp}
    #     return resp

    async def _get(self):
        params = helper.params_adapter(self.args)
        parsed_resp = {}

        async def process_query(idx, i, j):
            print("@@@ idx")
            print(idx)
            print("@@@ idx i")
            print(i)
            print("@@@ idx j")
            print(j)
            query = helper.create_query(idx, params, self.size)
            query_resp = await self.asynchronous_fetch(query)
            parsed_resp.update(helper.parse_response(query_resp, idx, params))
            idx = idx + 1

        tasks = [process_query(idx, i, j) for idx, i, j in create_iterator(params["pangolin_lineage"], params["mutations"])]
        await asyncio.gather(*tasks)

        resp = {"success": True, "results": parsed_resp}
        return resp
