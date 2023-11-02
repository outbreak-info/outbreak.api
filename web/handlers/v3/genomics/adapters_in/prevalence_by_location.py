import re
from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    if args.q is not None:
        params["q"] = args.q or None

        queries_delimiter = "|"
        params["q_list"] = args.q.split(queries_delimiter) if args.q is not None else []

        params["query_string_list"] = []
        for q in params["q_list"]:
            q_formatted = q.replace("lineages", "pangolin_lineage")
            keywords = ["mutations", "pangolin_lineage", "pangolin_lineage_crumbs"]
            pattern = rf'({"|".join(keywords)}):|:'
            q_formatted = re.sub(
                pattern, lambda match: match.group(0) if match.group(1) else r"\:", q_formatted
            )
            params["query_string_list"].append(q_formatted)

    params["pangolin_lineage"] = (
        args.pangolin_lineage.split(",") if args.pangolin_lineage is not None else []
    )

    params["mutations"] = args.mutations or None
    params["query_mutations"] = args.mutations.split(" AND ") if args.mutations is not None else []
    params["location_id"] = args.location_id or None
    params["cumulative"] = args.cumulative
    params["min_date"] = args.min_date or None
    params["max_date"] = args.max_date or None

    return params
