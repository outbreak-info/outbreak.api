import json
import logging
from pprint import pprint

import requests
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch_dsl import Search
from tornado.options import options, parse_command_line

options.define('host', default="api.outbreak.info:9200")
options.define('pattern', default="outbreak-resources-*")
options.define('url', default="https://raw.githubusercontent.com/outbreak-info/outbreak_preprint_matcher/main/results/update%20dumps/update_file.json")

def main():
    parse_command_line()
    try:
        client = Elasticsearch(options.host)
        # with open("update_file_initial.json") as file:
        #     updates = json.load(file)
        updates = requests.get(options.url).json()

        for update in updates:
            search = Search().using(client).query("match", _id=update['_id'])
            response = search.execute()
            if response.hits.total == 1:
                _index = response.hits.hits[0]['_index']
                _type = response.hits.hits[0]['_type']
                _correction = update['correction']
                assert isinstance(_correction, list)
                if 'correction' in response.hits.hits[0]:
                    if isinstance(response.hits.hits[0]['correction'], list):
                        _correction += response.hits.hits[0]['correction']
                    else:
                        _correction.append(response.hits.hits[0]['correction'])
                #-----------------------------------------------------------------------------------#
                client.update(_index, doc_type=_type, id=update['_id'], body={'doc': {
                    'correction': _correction
                }})
                #-----------------------------------------------------------------------------------#
            else:
                logging.error("id not unique.")

    except (TransportError, requests.exceptions.RequestException) as exc:
        logging.error(exc.info)


if __name__ == "__main__":
    main()
