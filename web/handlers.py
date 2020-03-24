import json
import logging
import os
import sys

import tornado.gen
import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web
from jinja2 import Environment, FileSystemLoader
from tornado.httputil import url_concat

import requests

log = logging.getLogger("pending")

src_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
if src_path not in sys.path:
    sys.path.append(src_path)

TEMPLATE_PATH = os.path.join(src_path, 'templates/static/html/')
templateLoader = FileSystemLoader(searchpath=TEMPLATE_PATH)
templateEnv = Environment(loader=templateLoader, cache_size=0)

def get_api_list():
    r = requests.get('https://biothings.ncats.io/api/list');
    return r.json()['result']

class BaseHandler(tornado.web.RequestHandler):
    def return_json(self, data):
        _json_data = json_encode(data)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(_json_data)

class MainHandler(BaseHandler):
    def get(self):
        list = get_api_list()
        index_file = "index.html"
        index_template = templateEnv.get_template(index_file)
        index_output = index_template.render(Context=json.dumps({"List": list}))
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
