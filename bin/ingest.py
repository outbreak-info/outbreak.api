from pprint import pprint

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

if __name__ == "__main__":
    try:
        client = Elasticsearch()
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
                                        return false
                                    }
                                    if (date.isBefore(now)) {
                                        ctx.date = ctx[field];
                                        return true;
                                    }
                                    return false
                                }
                                return false
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
    except RequestError as exc:
        pprint(exc.info, width=200)
