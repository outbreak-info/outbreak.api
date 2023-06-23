import web.handlers.v2.genomics.helpers.lineage_mutations_helper as helper

from web.handlers.genomics.base import BaseHandler


class LineageMutationsHandler(BaseHandler):
    name = "lineage-mutations"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str, "required": True},
        "frequency": {"type": float, "default": 0.8, "min": 0, "max": 1},
        "gene": {"type": str, "default": None},
    }

    async def _get(self):
        # Parse querystring parameters
        pangolin_lineage = self.args.pangolin_lineage
        frequency = self.args.frequency
        gene = self.args.gene
        genes = gene.lower().split(",") if gene else []

        query = helper.create_query(pangolin_lineage)
        self.observability.log("es_query_before", query)
        resp = await self.asynchronous_fetch(query)
        self.observability.log("es_query_after", query)
        dict_response = helper.parse_response(resp=resp, frequency=frequency, genes=genes)
        self.observability.log("transformations_after")
        result = {"success": True, "results": dict_response}

        return result
