import observability

from web.handlers.genomics.base import BaseHandler


class BaseHandlerV3(BaseHandler):

    def initialize(self):
        super().initialize(self)
        self.observability = observability.Observability()

    async def asynchronous_fetch(self, query):
        query["track_total_hits"] = True
        response = await self.biothings.elasticsearch.async_client.search(
            index=self.biothings.config.genomics.ES_INDEX_V3, body=query, size=0, request_timeout=90
        )
        return response

    async def asynchronous_fetch_count(self, query):
        query["track_total_hits"] = True
        response = await self.biothings.elasticsearch.async_client.count(
            index=self.biothings.config.genomics.ES_INDEX_V3, body=query
        )
        return response

    async def get_mapping(self):
        response = await self.biothings.elasticsearch.async_client.indices.get_mapping(
            index=self.biothings.config.genomics.ES_INDEX_V3
        )
        return response
