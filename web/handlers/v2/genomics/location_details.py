import web.handlers.v2.genomics.helpers.location_details as helper

from web.handlers.genomics.base import BaseHandler


class LocationDetailsHandler(BaseHandler):
    name = "location-lookup"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "id": {"type": str, "required": True},
    }

    async def _get(self):
        query_str = self.args.id
        query_ids = query_str.split("_")
        query = helper.create_query(query_ids=query_ids, query_str=query_str)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(query_resp=query_resp, query_ids=query_ids, query_str=query_str)
        resp = {"success": True, "results": parsed_resp}
        return resp
