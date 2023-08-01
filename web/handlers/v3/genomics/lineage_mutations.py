import web.handlers.v3.genomics.helpers.lineage_mutations_helper as helper

from web.handlers.v3.genomics.base import BaseHandlerV3


class LineageMutationsHandler(BaseHandlerV3):
    name = "lineage-mutations-v3"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "lineages": {"type": str, "required": True},
        "mutations": {"type": str},
        "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
        "gene": {"type": str, "default": None},
    }

    async def _get(self):
        lineages = self.args.lineages if self.args.lineages else ""
        mutations = self.args.mutations if self.args.mutations else ""
        frequency = self.args.frequency
        genes = self.args.gene.lower().split(",") if self.args.gene else []
        query = helper.create_query(lineages=lineages, mutations=mutations)
        self.observability.log("es_query_before", query)
        resp = await self.asynchronous_fetch(query=query)
        self.observability.log("es_query_after", query)
        dict_response = helper.parse_response(resp=resp, frequency=frequency, lineages=lineages, genes=genes)
        result = {"success": True, "results": dict_response}
        return result
