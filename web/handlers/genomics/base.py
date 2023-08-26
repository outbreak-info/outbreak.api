import abc

from biothings.web.handlers import BaseAPIHandler

from .gisaid_auth import gisaid_authorized

class BaseHandler(BaseAPIHandler):
    __metaclass__ = abc.ABCMeta

    kwargs = dict(BaseAPIHandler.kwargs)

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type,Authorization")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PATCH, PUT")

    size = 10000

    async def asynchronous_fetch(self, query):
        query["track_total_hits"] = True
        print("### query OLD")
        print(query)
        response = await self.biothings.elasticsearch.async_client.search(
            index=self.biothings.config.genomics.ES_INDEX, body=query, size=0, request_timeout=90
        )
        ### TODO: Remove FOR PROD
        response_new = await self.biothings.elasticsearch.async_client.search(
            index=self.biothings.config.genomics.ES_INDEX_V3, body=query, size=0, request_timeout=90
        )
        ### TODO: Remove FOR PROD
        if not _deep_compare(response["hits"], response_new["hits"]):
            # raise ValueError("### OLD AND NEW HAVE DIFFERENT VALUES ###")
            print("##########################################")
            print("### OLD AND NEW HAVE DIFFERENT VALUES ###")
            print("##########################################")
        else:
            # raise ValueError("### OLD AND NEW HAVE DIFFERENT VALUES ###")
            print("##########################################")
            print("### OLD AND NEW    E Q U A L    VALUES ###")
            print("##########################################")
        # print("### response")
        # print(response)
        return response

    async def asynchronous_fetch_count(self, query):
        query["track_total_hits"] = True
        response = await self.biothings.elasticsearch.async_client.count(
            index=self.biothings.config.genomics.ES_INDEX, body=query
        )
        # ### TODO: Remove FOR PROD
        # response_new = await self.biothings.elasticsearch.async_client.count(
        #     index=self.biothings.config.genomics.ES_INDEX_V3, body=query
        # )
        # ### TODO: Remove FOR PROD
        # if not _deep_compare(response["hits"], response_new["hits"]):
        #     raise ValueError("### OLD AND NEW HAVE DIFFERENT VALUES ###")
        return response

    async def get_mapping(self):
        response = await self.biothings.elasticsearch.async_client.indices.get_mapping(
            index=self.biothings.config.genomics.ES_INDEX
        )
        # ### TODO: Remove FOR PROD
        # response_new = await self.biothings.elasticsearch.async_client.indices.get_mapping(
        #     index=self.biothings.config.genomics.ES_INDEX_V3
        # )
        # ### TODO: Remove FOR PROD
        # if not _deep_compare(response["hits"], response_new["hits"]):
        #     raise ValueError("### OLD AND NEW HAVE DIFFERENT VALUES ###")

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




# TODO: Remove in PROD
def _deep_compare(dict1, dict2):
    print("dict1")
    print(dict1)
    print("dict2")
    print(dict2)

    if isinstance(dict1, dict) and isinstance(dict2, dict):
        if set(dict1.keys()) != set(dict2.keys()):
            print("IT'S DIFFERENT 0: " + str(set(dict1.keys())) + " | " + str(set(dict2.keys())) )
            return False

        for key in dict1.keys():
            if not _deep_compare(dict1[key], dict2[key]):
                print("IT'S DIFFERENT 1")
                return False
        return True
    elif isinstance(dict1, list) and isinstance(dict2, list):
        if len(dict1) != len(dict2):
            print("IT'S DIFFERENT - DICTS LEN: " + str(len(dict1)) + " | " + str(len(dict2)))
            print("#########A")
            print("   dict1: " + str(dict1))
            print("#########B")
            print("   dict2: " + str(dict2))
            return False

        for item1, item2 in zip(dict1, dict2):
            if not _deep_compare(item1, item2):
                print("IT'S DIFFERENT 3")
                return False
        return True
    else:
        return dict1 == dict2
