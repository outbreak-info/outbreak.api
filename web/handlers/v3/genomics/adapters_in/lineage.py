from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    params["query_str"] = args.name if args.name else None
    params["size"] = args.size if args.size else None
    return params
