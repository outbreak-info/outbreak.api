from pprint import pprint

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from tornado.options import options, parse_command_line


options.define('host', default="localhost:9200")
options.define('pattern', default="outbreak-resources-*")


if __name__ == "__main__":
    parse_command_line()
    try:
        client = Elasticsearch(options.host)
        client.ingest.put_pipeline('resources-common', {
            "description": "compose date field",
            "processors": [
                {
                    "set": {
                        "field": "_timestamp",
                        "value": "{{_ingest.timestamp}}"
                    }
                },
                {
                    "script": {
                        "source": """
                            boolean validDate(def ctx, def field, def now) {
                                if (ctx.containsKey(field)) {
                                    def date;
                                    try {
                                        date = LocalDate.parse(ctx[field], DateTimeFormatter.ISO_LOCAL_DATE);
                                    }
                                    catch(Exception e) {
                                        return false;
                                    }
                                    if (date.isAfter(now)) {
                                        return false;
                                    }
                                    ctx.date = ctx[field];
                                    return true;
                                }
                                return false;
                            }
                            LocalDate now = LocalDate.parse(ctx._timestamp, DateTimeFormatter.ISO_ZONED_DATE_TIME);
                            if(validDate(ctx, 'dateModified', now)){ return }
                            if(validDate(ctx, 'datePublished', now)){ return }
                            if(validDate(ctx, 'dateCreated', now)){ return }
                            ctx.date = null;
                        """.replace('\n', ' ')
                    }
                },
                {
                    "remove": {
                        "field": "_timestamp"
                    }
                }
            ]
        })
        client.indices.put_template("resources-common", {
            "index_patterns": [
                options.pattern
            ],
            "settings": {
                "index": {
                    "number_of_shards": "1",
                    "number_of_replicas": "0",
                    "default_pipeline": "resources-common"
                }
            },
            "mappings": {},
            "aliases": {}
        })
    except TransportError as exc:
        pprint(exc.info, indent=4, width=500)
