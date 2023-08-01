import web.handlers.v3.genomics.helpers.location_details_helper as helper

from web.handlers.v3.genomics.base import BaseHandlerV3


class LocationDetailsHandler(BaseHandlerV3):
    name = "location-lookup"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "id": {"type": str, "required": True},
    }

    async def _get(self):
        query_str = self.args.id
        query_ids = query_str.split("_")
        query = helper.create_query(query_ids=query_ids, query_str=query_str)
        self.observability.log("es_query_before", query)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(resp=query_resp, query_ids=query_ids, query_str=query_str)
        resp = {"success": True, "results": parsed_resp}
        return resp
