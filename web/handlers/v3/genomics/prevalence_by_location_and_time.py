import web.handlers.v3.genomics.helpers.prevalence_by_location_helper as helper

from web.handlers.v3.genomics.base import BaseHandlerV3


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

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params, self.size)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(query_resp, params)
        resp = {"success": True, "results": parsed_resp}
        return resp
