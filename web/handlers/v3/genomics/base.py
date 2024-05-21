import observability

# Third-party imports
from web.handlers.genomics.base import BaseHandler


class BaseHandlerV3(BaseHandler):
    size = 10000

    def initialize(self):
        super().initialize()
        self.observability = observability.Observability()

    async def asynchronous_fetch_lineages(self, query):
        query["track_total_hits"] = True
        response = await self.biothings.elasticsearch.async_client.search(
            index=self.biothings.config.genomics.ES_MUTLESS_INDEX,
            body=query,
            request_timeout=150,
        )
        return response

    async def asynchronous_fetch_mutations(self, query):
        query["track_total_hits"] = True
        response = await self.biothings.elasticsearch.async_client.search(
            index=self.biothings.config.genomics.ES_MUTS_INDEX,
            body=query,
            request_timeout=150,
        )
        return response
