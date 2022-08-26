"""
Non-API handlers go here, e.g. the landing page and API page.
"""

import tornado.web
from tornado.escape import json_encode
from jinja2 import Environment, FileSystemLoader

templateLoader = FileSystemLoader(searchpath='web/templates')
templateEnv = Environment(loader=templateLoader, cache_size=0)

def get_api_list():
    res = [
        {
            "_id": "covid19",
            "config": {
                "doc_type": "outbreak_info"
            },
            "description": "COVID19 live outbreak data",
            "status": "running",
            "link": False
        },
        {
            "_id": "resources",
            "config": {
                "doc_type": "resource"
            },
            "description": "COVID19 collection of datasets, publications ,clinical trials, protocols, and more.",
            "status": "running",
            "link": False
        },
        {
            "_id": "genomics",
            "config": {
                "doc_type": "mutation"
            },
            "description": "Provides access to the underlying genomic and epidemiology data on outbreak.info.",
            "status": "running",
            "link": "https://outbreak-info.github.io/R-outbreak-info/"
        },
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
    def get(self):
        view_file = "try.html"
        view_template = templateEnv.get_template(view_file)
        view_output = view_template.render()
        self.write(view_output)

class SpecialHandler(BaseHandler):
    def get(self):
        view_file = "try-resources.html"
        view_template = templateEnv.get_template(view_file)
        view_output = view_template.render()
        self.write(view_output)
