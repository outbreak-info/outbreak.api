from datetime import timedelta
from scipy.stats import beta
import pandas as pd

def calculate_proportion(x, n):
    x = x.round()
    n = n.round()
    ci_low, ci_upp = beta.interval(1 - 0.05, x + 0.5, n - x + 0.5) # Jeffreys Interval
    est_proportion = x/n
    return est_proportion, ci_low, ci_upp

def compute_rolling_mean(df, index_col, col, new_col):
    df = df.set_index(index_col)
    df.loc[:,new_col] = df[col].rolling("7d").mean()
    df = df.reset_index()
    return df

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
        df_response = compute_rolling_mean(df_response, "date", "total_count", "total_count_rolling")
        df_response = compute_rolling_mean(df_response, "date", "lineage_count", "lineage_count_rolling")
        d = calculate_proportion(df_response["lineage_count_rolling"], df_response["total_count_rolling"])
        df_response.loc[:, "proportion"] = d[0]
        df_response.loc[:, "proportion_ci_lower"] = d[1]
        df_response.loc[:, "proportion_ci_upper"] = d[2]
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        dict_response = df_response.to_dict(orient="records")
    else:                       # For cumulative only calculate cumsum prevalence
        if df_response.shape[0] == 0:
            dict_response = {
                "global_prevalence": 0,
                "total_count": 0,
                "lineage_count": 0,
                "first_detected": None,
                "last_detected": None
            }
        else:
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

def compute_cumulative(grp, cols):
    grp = grp.sort_values("date")
    first_date = grp[grp["lineage_count"] > 0]["date"].min()
    tmp_grp = grp[grp["date"] >= first_date]
    if tmp_grp.shape[0] != 0:
        for i in cols:
            tmp_grp.loc[:, "cum_{}".format(i)] = tmp_grp[i].cumsum()
            tmp_grp.loc[:, "cum_{}".format(i)] = tmp_grp[i].cumsum()
        return tmp_grp.tail(1)
    else:
        for i in cols:
            if i == "total_count":
                grp.loc[:, "cum_total_count"] = grp["total_count"].cumsum()
            else:
                grp.loc[:, "cum_{}".format(i)] = 0
        return grp.tail(1)

def transform_prevalence_by_location_and_tiime(flattened_response, query_detected = False):
    df_response = (
        pd.DataFrame(flattened_response)
        .assign(date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
        .sort_values("date")
    )
    grps = []
    dict_response = {}
    if not query_detected:
        df_response =  df_response.groupby("name").apply(compute_cumulative, ["total_count", "lineage_count"])
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        d = calculate_proportion(df_response["cum_lineage_count"], df_response["cum_total_count"])
        df_response.loc[:, "proportion"] = d[0]
        df_response.loc[:, "proportion_ci_lower"] = d[1]
        df_response.loc[:, "proportion_ci_upper"] = d[2]
        dict_response = df_response.to_dict(orient="records")
    else:
        dict_response = {
            "names": df_response[df_response["lineage_count"] > 0]["name"].unique().tolist()
        }
    return dict_response

def create_nested_mutation_query(country = None, division = None, lineage = None, mutations = []):
    query_obj = {
        "bool": {
            "must": []
        }
    }
    bool_must = []
    for i in mutations:
        bool_must.append({
            "nested": {
                "path": "mutations",
                "query": {
                    "term" : { "mutations.mutation" : i }
                }
            }
        })
    if lineage is not None:
        bool_must.append({
            "term": {
                "pangolin_lineage": lineage
            }
        })
    if country is not None:
        bool_must.append({
            "term": {
                "country": country
            }
        })
    if division is not None:
        bool_must.append({
            "term": {
                "division": division
            }
        })
    query_obj["bool"]["must"] = bool_must
    return query_obj

def classify_other_category(grp, keep_lineages):
    grp.loc[(~grp["lineage"].isin(keep_lineages)) | (grp["lineage"] == "none"), "lineage"] = "other" # Temporarily remove none. TODO: Proper fix
    grp = grp.groupby("lineage").agg({
        "total_count": lambda x: x.iloc[0],
        "lineage_count": "sum"
    })
    return grp

def get_major_lineage_prevalence(df, index_col, keep_lineages = [], prevalence_threshold = 0.05, nday_threshold = 0.05):
    ndays = (df[index_col].iloc[-1] - df[index_col].iloc[0]).days
    lineages_to_retain = df[df["prevalence"] >= prevalence_threshold]["lineage"].value_counts()
    lineages_to_retain = lineages_to_retain[lineages_to_retain >= nday_threshold * ndays].index.tolist()
    lineages_to_retain.extend(keep_lineages)
    df = df.groupby(index_col).apply(classify_other_category, lineages_to_retain)
    df = df.reset_index()
    df.loc[:,"prevalence"] = df["lineage_count"]/df["total_count"]
    return df
