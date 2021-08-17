from biothings.web.handlers import BaseAPIHandler

class BaseHandler(BaseAPIHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.add_header("Access-Control-Allow-Headers", "Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PATCH, PUT')

    size = 10000

    async def asynchronous_fetch(self, query):
        response = await self.web_settings.connections.async_client.search(
            index = "outbreak-genomics",
            body = query,
            size = 0
        )
        return response

    async def asynchronous_fetch_count(self, query):
        response = await self.web_settings.connections.async_client.count(
            index = "outbreak-genomics",
            body = query
        )
        return response

    def post(self):
        pass

