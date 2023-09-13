import web.handlers.v3.genomics.helpers.lineage_mutations_helper as helper
from web.handlers.v3.genomics.base import BaseHandlerV3


class LineageMutationsHandler(BaseHandlerV3):
    name = "lineage-mutations-v3"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str},
        "lineages": {"type": str},
        "mutations": {"type": str},
        "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
        "gene": {"type": str, "default": None},
    }

    async def _get(self):
        params = helper.params_adapter(self.args)
        query = helper.create_query(lineages=params["lineages"], mutations=params["mutations"])
        self.observability.log("es_query_before", query)
        resp = await self.asynchronous_fetch(query=query)
        self.observability.log("es_query_after", query)
        dict_response = helper.parse_response(
            resp=resp, frequency=params["frequency"], lineages=params["lineages"], genes=params["genes"]
        )
        result = {"success": True, "results": dict_response}
        return result
