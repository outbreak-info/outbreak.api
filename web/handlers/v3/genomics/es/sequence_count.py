from typing import Dict

from elasticsearch_dsl import Q, Search

from web.handlers.v3.genomics.util import parse_location_id_to_query


def create_query(params: Dict = None, size: int = None) -> Dict:
    s = Search()

    if params is None:
        params = {}

    if size is not None:
        s = s.extra(size=size)

    if params.get("location_id"):
        location_query = parse_location_id_to_query(params["location_id"])
        s = s.query(location_query)

    if not params.get("cumulative"):
        s = s.extra(size=0)
        s.aggs.bucket("date", "terms", field="date_collected", size=size)
    else:
        if not s.query:
            s = s.query(Q("exists", field="pangolin_lineage"))
        else:
            s = s.query(Q("bool", must=[s.query, Q("exists", field="pangolin_lineage")]))

        if params.get("subadmin"):
            subadmin = None
            if not params.get("location_id"):
                subadmin = "country_id"
            elif len(params["location_id"].split("_")) == 1:  # Country
                subadmin = "division_id"
            elif len(params["location_id"].split("_")) == 2:  # Division
                subadmin = "location_id"

            if subadmin:
                s.aggs.bucket("subadmin", "terms", field=subadmin, size=size)

    return s.to_dict()
