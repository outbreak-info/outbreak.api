from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import parse_location_id_to_query


class LocationDetailsHandler(BaseHandler):
    name = "location-lookup"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "id": {"type": str, "required": True},
    }

    async def _get(self):
        query_str = self.args.id
        query_ids = query_str.split("_")
        query = {"query": {}, "aggs": {"loc": {"composite": {"size": 10000, "sources": []}}}}
        loc_id_len = len(query_ids)
        if loc_id_len >= 1:
            query["aggs"]["loc"]["composite"]["sources"].extend(
                [
                    {"country": {"terms": {"field": "country"}}},
                    {"country_id": {"terms": {"field": "country_id"}}},
                ]
            )
        if loc_id_len >= 2:  # 3 is max length
            query["aggs"]["loc"]["composite"]["sources"].extend(
                [
                    {"division": {"terms": {"field": "division"}}},
                    {"division_id": {"terms": {"field": "division_id"}}},
                ]
            )
        if loc_id_len == 3:  # 3 is max length
            query["aggs"]["loc"]["composite"]["sources"].extend(
                [
                    {"location": {"terms": {"field": "location"}}},
                    {"location_id": {"terms": {"field": "location_id"}}},
                ]
            )
        query["query"] = parse_location_id_to_query(query_str)
        resp = await self.asynchronous_fetch(query)
        flattened_response = []
        for rec in resp["aggregations"]["loc"]["buckets"]:
            if loc_id_len == 1:
                flattened_response.append(
                    {
                        "country": rec["key"]["country"],
                        "country_id": rec["key"]["country_id"],
                        "label": rec["key"]["country"],
                        "admin_level": 0,
                    }
                )
            elif loc_id_len == 2:
                flattened_response.append(
                    {
                        "division": rec["key"]["division"],
                        "division_id": rec["key"]["division_id"],
                        "country": rec["key"]["country"],
                        "country_id": rec["key"]["country_id"],
                        "label": ", ".join([rec["key"]["division"], rec["key"]["country"]]),
                        "admin_level": 1,
                    }
                )
            elif loc_id_len == 3:
                flattened_response.append(
                    {
                        "location": rec["key"]["location"],
                        "location_id": rec["key"]["location_id"],
                        "division": rec["key"]["division"],
                        "division_id": rec["key"]["division_id"],
                        "country": rec["key"]["country"],
                        "country_id": rec["key"]["country_id"],
                        "label": ", ".join(
                            [rec["key"]["location"], rec["key"]["division"], rec["key"]["country"]]
                        ),
                        "admin_level": 2,
                    }
                )
        if len(flattened_response) >= 1:
            flattened_response = flattened_response[0]  # ID should match only 1 region
        flattened_response["query_id"] = query_str
        resp = {"success": True, "results": flattened_response}
        return resp
