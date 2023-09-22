from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    mutations = args.mutations.replace(",", " OR ")
    params["mutations"] = mutations
    return params
