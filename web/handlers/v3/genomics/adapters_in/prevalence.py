from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    params["pangolin_lineage"] = args.pangolin_lineage or None
    params["mutations"] = args.mutations or None
    params["cumulative"] = args.cumulative
    return params
