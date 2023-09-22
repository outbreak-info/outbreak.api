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
            keywords = ["mutations", "pangolin_lineage"]
            pattern = rf'({"|".join(keywords)}):|:'
            q_formatted = re.sub(
                pattern, lambda match: match.group(0) if match.group(1) else r"\:", q_formatted
            )
            params["query_string_list"].append(q_formatted)

    params["pangolin_lineage"] = args.pangolin_lineage or None
    params["mutations"] = args.mutations or None
    params["mutations_list"] = args.mutations.split(",") if args.mutations is not None else []
    params["location_id"] = args.location_id or None
    params["frequency"] = args.frequency
    return params
