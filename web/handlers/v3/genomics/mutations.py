import web.handlers.v3.genomics.helpers.mutations_helper as helper

from web.handlers.v3.genomics.base import BaseHandlerV3

# from web.handlers.genomics.base import BaseHandler


class MutationHandler(BaseHandlerV3):
    name = "mutations"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "name": {"type": str, "required": True},
    }

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(params)
        query_resp = await self.asynchronous_fetch(query)
        parsed_resp = helper.parse_response(resp=query_resp)
        resp = {"success": True, "results": parsed_resp}
        return resp


# class MutationHandler(BaseHandler):
#     name = "mutations"
#     kwargs = dict(BaseHandler.kwargs)
#     kwargs["GET"] = {
#         "name": {"type": str, "required": True},
#     }

#     async def _get(self):
#         query_str = self.args.name
#         query = {
#             "size": 0,
#             "query": {
#                 "query_string": {
#                 "query": query_str # Ex: "mutation: \"ORF1a:A735A\" OR \"ORF1a:P3395H\""
#                 }
#             },
#             "aggs": {
#                 "by_name": {
#                     "terms": {
#                         "field": "mutation"
#                     }
#                 }
#             }
#         }
#         resp = await self.asynchronous_fetch(query)
#         path_to_results = [
#             "aggregations",
#             "mutations",
#             "mutation_filter",
#             "count_filter",
#             "buckets",
#         ]
#         buckets = resp
#         for i in path_to_results:
#             buckets = buckets[i]
#         flattened_response = [{"name": i["key"], "total_count": i["doc_count"]} for i in buckets]
#         resp = {"success": True, "results": flattened_response}
#         return resp
