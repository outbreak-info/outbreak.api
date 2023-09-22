from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    params["location_id"] = args.location_id or None
    params["cumulative"] = args.cumulative
    params["subadmin"] = args.subadmin
    print(params)
    return params
