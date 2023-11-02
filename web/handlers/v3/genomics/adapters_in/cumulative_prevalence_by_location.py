from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    params["query_pangolin_lineage"] = args.pangolin_lineage
    params["query_pangolin_lineage"] = (
        params["query_pangolin_lineage"].split(",")
        if params["query_pangolin_lineage"] is not None
        else []
    )
    params["query_detected"] = args.detected
    params["query_mutations"] = args.mutations
    params["query_location"] = args.location_id
    params["query_mutations"] = (
        params["query_mutations"].split(" AND ") if params["query_mutations"] is not None else []
    )
    params["query_ndays"] = args.ndays

    return params
