def parse_response(resp = {}, size = None):
    path_to_results = ["aggregations", "prevalence", "country", "buckets"]
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = [{"key": i["key"], "doc_count": i["doc_count"]} for i in buckets]
    if size:
        try:
            size = int(size)
        except Exception:
            return {"success": False, "results": [], "errors": "Invalide size value"}
        flattened_response = sorted(flattened_response, key=lambda x: -x["total_count"])
        flattened_response = flattened_response[:size]
    return flattened_response
