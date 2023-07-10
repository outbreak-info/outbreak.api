import web.handlers.v2.genomics.helpers.lineage_mutations_helper as helper

from web.handlers.genomics.base import BaseHandler


class LineageMutationsHandler(BaseHandler):
    name = "lineage-mutations"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "lineages": {"type": str, "required": True},
        "mutations": {"type": str},
        "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
        "gene": {"type": str, "default": None},
    }

    async def _get(self):
        # Parse querystring parameters
        lineages = self.args.lineages if self.args.lineages else ""
        mutations = self.args.mutations if self.args.mutations else ""
        frequency = self.args.frequency
        genes = self.args.gene.lower().split(",") if self.args.gene else []

        query = helper.create_query(lineages=lineages, mutations=mutations)
        self.observability.log("es_query_before", query)
        resp = await self.asynchronous_fetch(query=query)
        self.observability.log("es_query_after", query)
        dict_response = helper.parse_response(resp=resp, frequency=frequency, genes=genes)
        self.observability.log("transformations_after")

        result = {"success": True, "results": dict_response}

        return result
