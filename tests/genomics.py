from tornado.testing import AsyncHTTPTestCase
from tornado.web     import Application
import tornado.ioloop

from web.handlers.genomics import routes
from elasticsearch import Elasticsearch

async def asynchronous_fetch(self, query):
    print('ah')
    print(query)
    es = Elasticsearch(['localhost'], scheme='http', port=9200)
    response = await es.search(
        index = "outbreak-genomics",
        body = query,
        size = 0
    )
    return response

async def asynchronous_fetch_count(self, query):
    client = AsyncElasticsearch(hosts=['http://localhost:9200'])
    response = await client.search(
        index = "outbreak-genomics",
        body = query
    )
    return response


class TestGenomics(AsyncHTTPTestCase):
    def get_app(self):
        for _, handler in routes:
            handler.asynchronous_fetch = asynchronous_fetch
            handler.asynchronous_fetch_count = asynchronous_fetch_count
        app = Application(routes)
        app.listen(62706)
        tornado.ioloop.IOLoop.current().start()
        print(app)
        return app

    def _test_seq_count(res):
        assert res.get('success') 
        assert res['success'] == True
        assert res.get('results')
        assert len(res['results'])
        res0 = res['results'][0]
        assert type(res0['total_count']) is int
        assert datetime.strptime(res0['date'], '%Y-%m-%d')

    def test_seq_counts_1(self):
        res = self.fetch('/genomics/sequence-count', method="GET")
        print(res)
        return
        res_json = res.json()
        print(res)
        test_seq_count(res)

    def test_seq_counts_2(self):
        pass
        #res = self.request('genomics/sequence-count?location_id=USA&cumulative=true&subadmin=true').json()
        #test_seq_count(res)

#t = TestGenomics()
#t.get_app()
