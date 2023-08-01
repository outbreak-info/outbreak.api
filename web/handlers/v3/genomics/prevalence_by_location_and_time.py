from web.handlers.v3.genomics.base import BaseHandlerV3
from web.handlers.v3.genomics.util import (
    create_nested_mutation_query,
    create_query_filter,
    parse_location_id_to_query,
    transform_prevalence,
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

    async def _get(self):
        query_location = self.args.location_id
        query_pangolin_lineage = self.args.pangolin_lineage
        # query_pangolin_lineage = (
        #     query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
        # )
        query_mutations = self.args.mutations
        # query_mutations = query_mutations.split(" AND ") if query_mutations is not None else []
        cumulative = self.args.cumulative
        date_range_filter = {"query": {"range": {"date_collected": {}}}}
        if self.args.max_date:
            date_range_filter["query"]["range"]["date_collected"]["lte"] = self.args.max_date
        if self.args.min_date:
            date_range_filter["query"]["range"]["date_collected"]["gte"] = self.args.min_date

        results = {}
        # for i, j in create_iterator(query_pangolin_lineage, query_mutations):
        query = {
            "size": 0,
            "aggs": {
                "prevalence": {
                    "filter": {"bool": {"must": []}},
                    "aggs": {
                        "count": {
                            "terms": {"field": "date_collected", "size": self.size},
                            "aggs": {"lineage_count": {"filter": {}}},
                        }
                    },
                }
            },
        }
        if self.args.max_date or self.args.min_date:
            query.update(date_range_filter)
        parse_location_id_to_query(query_location, query["aggs"]["prevalence"]["filter"])
        # lineages = i.split(" OR ") if i is not None else []
        lineages = query_pangolin_lineage if query_pangolin_lineage is not None else ""
        mutations = query_mutations if query_mutations is not None else ""
        query_obj = create_nested_mutation_query(
            lineages=lineages, mutations=mutations, location_id=query_location
        )
        query["aggs"]["prevalence"]["aggs"]["count"]["aggs"]["lineage_count"][
            "filter"
        ] = query_obj
        resp = await self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "prevalence", "count", "buckets"]
        resp = transform_prevalence(resp, path_to_results, cumulative)
        # TODO: What should be returned as `res_key`?
        # res_key = None
        # if len(query_pangolin_lineage) > 0:
        #     res_key = " OR ".join(lineages)
        # if len(query_mutations) > 0:
        #     res_key = (
        #         "({}) AND ({})".format(res_key, " AND ".join(query_mutations))
        #         if res_key is not None
        #         else " AND ".join(query_mutations)
        #     )
        # TODO: Trying to keep a similar behavior for `res_key` for now.
        res_key = create_query_filter(lineages=lineages, mutations=mutations, locations=query_location)
        res_key = res_key.replace("pangolin_lineage.keyword: ", "")
        res_key = res_key.replace("mutations.keyword: ", "")
        res_key = res_key.replace("country_id.keyword: ", "")
        res_key = res_key.replace("\\", "")
        results[res_key] = resp
        return {"success": True, "results": results}
