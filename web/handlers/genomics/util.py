from datetime import timedelta
from scipy.stats import beta
import pandas as pd

def calculate_proportion(x, n):
    x = x.round()
    n = n.round()
    ci_low, ci_upp = beta.interval(1 - 0.05, x + 0.5, n - x + 0.5) # Jeffreys Interval
    est_proportion = x/n
    return est_proportion, ci_low, ci_upp

def transform_prevalence(resp, path_to_results = [], cumulative = False):
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    if len(buckets) == 0:
        return {"success": True, "results": []}
    flattened_response = [{
        "date": i["key"],
        "total_count": i["doc_count"],
        "lineage_count": i["lineage_count"]["doc_count"]
    } for i in buckets if len(i["key"].split("-")) > 1 and "XX" not in i["key"]]
    df_response = (
        pd.DataFrame(flattened_response)
        .assign(date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
        .sort_values("date")
    )
    first_date = df_response[df_response["lineage_count"] > 0]["date"].min()
    df_response = df_response[df_response["date"] >= first_date]
    dict_response = {}
    if not cumulative:
        df_response.loc[:,"total_count_rolling"] =  df_response.apply(lambda x: df_response[
            (df_response["date"] >= x["date"] - timedelta(days = 3)) &
            (df_response["date"] <= x["date"] + timedelta(days = 3))
        ]["total_count"].mean(), axis = 1)
        df_response.loc[:,"lineage_count_rolling"] =  df_response.apply(lambda x: df_response[
            (df_response["date"] >= x["date"] - timedelta(days = 3)) &
            (df_response["date"] <= x["date"] + timedelta(days = 3))
        ]["lineage_count"].mean(), axis = 1)
        d = calculate_proportion(df_response["lineage_count_rolling"], df_response["total_count_rolling"])
        df_response.loc[:, "proportion"] = d[0]
        df_response.loc[:, "proportion_ci_lower"] = d[1]
        df_response.loc[:, "proportion_ci_upper"] = d[2]
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        dict_response = df_response.to_dict(orient="records")
    else:                       # For cumulative only calculate cumsum prevalence
        lineage_cumsum = int(df_response["lineage_count"].cumsum().iloc[-1])
        total_cumsum = int(df_response["total_count"].cumsum().iloc[-1])
        df_date_sorted = df_response[df_response["lineage_count"] > 0].sort_values("date")
        dict_response = {
            "global_prevalence": lineage_cumsum/total_cumsum,
            "total_count": total_cumsum,
            "lineage_count": lineage_cumsum,
            "first_detected": df_date_sorted["date"].iloc[0].strftime("%Y-%m-%d"),
            "last_detected": df_date_sorted["date"].iloc[-1].strftime("%Y-%m-%d")
        }
    return {"success": True, "results": dict_response}

def transform_prevalence_by_location_and_tiime(flattened_response):
    df_response = (
        pd.DataFrame(flattened_response)
        .assign(date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
        .sort_values("date")
    )
    grps = []
    for n,grp in df_response.groupby("name"):
        grp = grp.sort_values("date")
        first_date = grp[grp["lineage_count"] > 0]["date"].min()
        tmp_grp = grp[grp["date"] >= first_date]
        if tmp_grp.shape[0] != 0:
            tmp_grp.loc[:, "cum_total_count"] = tmp_grp["total_count"].cumsum()
            tmp_grp.loc[:, "cum_lineage_count"] = tmp_grp["lineage_count"].cumsum()
            grps.append(tmp_grp.tail(1))
        else:
            grp.loc[:, "cum_total_count"] = grp["total_count"].cumsum()
            grp.loc[:, "cum_lineage_count"] = 0
            grps.append(grp.tail(1))
    df_response = pd.concat(grps)
    df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    d = calculate_proportion(df_response["cum_lineage_count"], df_response["cum_total_count"])
    df_response.loc[:, "proportion"] = d[0]
    df_response.loc[:, "proportion_ci_lower"] = d[1]
    df_response.loc[:, "proportion_ci_upper"] = d[2]
    dict_response = df_response.to_dict(orient="records")
    return dict_response

