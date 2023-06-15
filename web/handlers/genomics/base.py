import abc
import diskcache
import json

from biothings.web.handlers import BaseAPIHandler

from .gisaid_auth import gisaid_authorized

class BaseHandler(BaseAPIHandler):
    __metaclass__ = abc.ABCMeta

    kwargs = dict(BaseAPIHandler.kwargs)

    # prepare is called at the beginning of request handling
    def prepare(self):
        super().prepare()
        # Create cache and expires it in 7 days
        self.cache = diskcache.Cache("cache/genomics/",
                                    expire=604800,
                                    size_limit=1000000000,  # 1 GB disk limit
                                    eviction_policy="least-recently-used",  # Least Recently Used eviction policy
                                    compress_level=6
        )

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type,Authorization")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PATCH, PUT")

    size = 10000

    async def asynchronous_fetch(self, query):
        # Convert the query dictionary to a JSON string
        query_key = json.dumps(query, sort_keys=True)
        # Check if the response is already in the cache
        if query_key in self.cache:
            response = self.cache[query_key]
        else:
            query["track_total_hits"] = True
            response = await self.biothings.elasticsearch.async_client.search(
                index=self.biothings.config.genomics.ES_INDEX, body=query, size=0, request_timeout=90
            )
            # Store the response in the cache
            self.cache[query_key] = response
        return response

    async def asynchronous_fetch_count(self, query):
        query["track_total_hits"] = True
        response = await self.biothings.elasticsearch.async_client.count(
            index=self.biothings.config.genomics.ES_INDEX, body=query
        )
        return response

    async def get_mapping(self):
        response = await self.biothings.elasticsearch.async_client.indices.get_mapping(
            index=self.biothings.config.genomics.ES_INDEX
        )
        return response

    def post(self):
        pass

    async def get(self):
        if not getattr(self.biothings.config, "DISABLE_GENOMICS_ENDPOINT", False):
            await self._get_with_gisauth()
        else:
            resp = await self._get()
            self.write(resp)

    @gisaid_authorized
    async def _get_with_gisauth(self):
        resp = await self._get()
        self.write(resp)

    def _get(self):
        raise NotImplementedError()
