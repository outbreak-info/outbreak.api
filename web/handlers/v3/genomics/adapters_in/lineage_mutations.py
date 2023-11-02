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

    params["lineages"] = args.lineages if args.lineages else ""
    if params["lineages"] is None or params["lineages"] == "":
        params["lineages"] = args.pangolin_lineage if args.pangolin_lineage else ""
    params["mutations"] = args.mutations if args.mutations else ""
    params["frequency"] = args.frequency
    params["genes"] = args.gene.lower().split(",") if args.gene else []

    return params
