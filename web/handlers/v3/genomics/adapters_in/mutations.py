from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    mutations = args.name
    params["mutations"] = mutations
    return params
