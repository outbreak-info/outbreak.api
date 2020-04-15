"""
Non-API handlers go here, e.g. the landing page and API page.
"""
import os.path

import tornado.web
from tornado.escape import json_encode
from jinja2 import Environment, FileSystemLoader
# import requests

src_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
# import sys
# if src_path not in sys.path:
#     sys.path.append(src_path)

TEMPLATE_PATH = os.path.join(src_path, 'web/templates')
templateLoader = FileSystemLoader(searchpath=TEMPLATE_PATH)
templateEnv = Environment(loader=templateLoader, cache_size=0)

def get_api_list():
    # import requests
    # r = requests.get('https://api.outbreak.info/api/list')
    # res = r.json()['result']
    res = [
        {
            "_id": "covid19",
            "config": {
                "doc_type": "outbreak_info"
            },
            "description": "COVID19 live outbreak data",
            "status": "running"
        }
    ]
    return res

class BaseHandler(tornado.web.RequestHandler):
    def return_json(self, data):
        _json_data = json_encode(data)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(_json_data)

class MainHandler(BaseHandler):
    def get(self):
        api_list = get_api_list()
        index_file = "index.html"
        index_template = templateEnv.get_template(index_file)
        index_output = index_template.render(Context=json_encode({"List": api_list}))
        self.write(index_output)

class ApiViewHandler(BaseHandler):
    def get(self, namespace=None, className=None):
        view_file = "try.html"
        view_template = templateEnv.get_template(view_file)
        view_output = view_template.render()
        self.write(view_output)

APP_LIST = [
    (r"/?", MainHandler),
    (r"/(.+)/?", ApiViewHandler),
]
