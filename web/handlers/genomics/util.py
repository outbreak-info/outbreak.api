from datetime import timedelta, datetime as dt
from scipy.stats import beta
import pandas as pd

def calculate_proportion(_x, _n):
    x = _x.round()
    n = _n.round()
    ci_low, ci_upp = beta.interval(1 - 0.05, x + 0.5, n - x + 0.5) # Jeffreys Interval
    est_proportion = _x/_n
    return est_proportion, ci_low, ci_upp

def compute_total_count(df, col, new_col):
    df.loc[:,new_col] = df[col].sum()
    return df

def expand_dates(df, date_min, date_max, index_col, grp_col):
    idx = pd.date_range(date_min, date_max)
    df = (
        df
        .set_index(index_col)
        .reindex(idx, fill_value = 0)
        .drop(grp_col, axis = 1)
        .reset_index()
        .rename(
            columns = {
                "index": "date"
            }
        )
    )
    return df

def compute_rolling_mean_all_lineages(df, index_col, col, new_col, grp_col):
    idx = pd.date_range(df[index_col].min(), df[index_col].max())
    df = (
        df
        .set_index(index_col)
        .reindex(idx, fill_value = 0)
        .assign(**{
            new_col: lambda x: x[col].rolling("7d").mean()
        })
        .drop(grp_col, axis = 1)
        .reset_index()
        .rename(
            columns = {
                "index": "date"
            }
        )
    )
    return df

def compute_rolling_mean(df, index_col, col, new_col):
    df = (
        df
        .set_index(index_col)
        .assign(**{new_col: lambda x: x[col].rolling("7d").mean()})
        .reset_index()
    )
    return df

def transform_prevalence(resp, path_to_results = [], cumulative = False):
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    if len(buckets) == 0:
        return {"success": True, "results": {}}
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
    dict_response = {}
    if not cumulative:
        df_response = df_response[df_response["date"] >= first_date - pd.to_timedelta(6, unit='d')] # Go back 6 days for total_rolling
        df_response = compute_rolling_mean(df_response, "date", "total_count", "total_count_rolling")
        df_response = compute_rolling_mean(df_response, "date", "lineage_count", "lineage_count_rolling")
        df_response = df_response[df_response["date"] >= first_date] # Revert back to first date after total_rolling calculations are complete
        d = calculate_proportion(df_response["lineage_count_rolling"], df_response["total_count_rolling"])
        df_response.loc[:, "proportion"] = d[0]
        df_response.loc[:, "proportion_ci_lower"] = d[1]
        df_response.loc[:, "proportion_ci_upper"] = d[2]
        df_response.loc[:,"date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        dict_response = df_response.to_dict(orient="records")
    else:                       # For cumulative only calculate cumsum prevalence
        df_response = df_response[df_response["date"] >= first_date]
        if df_response.shape[0] == 0:
            dict_response = {
                "global_prevalence": 0,
                "total_count": 0,
                "lineage_count": 0,
                "first_detected": None,
                "last_detected": None
            }
        else:
            lineage_cumsum = int(df_response["lineage_count"].sum())
            total_cumsum = int(df_response["total_count"].sum())
            df_date_sorted = df_response[df_response["lineage_count"] > 0].sort_values("date")
            dict_response = {
                "global_prevalence": lineage_cumsum/total_cumsum,
                "total_count": total_cumsum,
                "lineage_count": lineage_cumsum,
                "first_detected": df_date_sorted["date"].iloc[0].strftime("%Y-%m-%d"),
                "last_detected": df_date_sorted["date"].iloc[-1].strftime("%Y-%m-%d")
            }
    return dict_response

def compute_cumulative(grp, cols):
    grp = grp.sort_values("date")
    if grp.shape[0] != 0:
        for i in cols:
            grp.loc[:, "cum_{}".format(i)] = grp[i].cumsum()
            grp.loc[:, "cum_{}".format(i)] = grp[i].cumsum()
        return grp.tail(1)
    else:
        for i in cols:
            if i == "total_count":
                grp.loc[:, "cum_total_count"] = grp["total_count"].cumsum()
            else:
                grp.loc[:, "cum_{}".format(i)] = 0
        return grp.tail(1)

def transform_prevalence_by_location_and_tiime(flattened_response, ndays = None, query_detected = False):
    df_response = (
        pd.DataFrame(flattened_response)
        .assign(date = lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
        .sort_values("date")
    )
    grps = []
    dict_response = {}
    if not query_detected:
        if ndays is not None:
            date_limit = dt.today() - timedelta(days = ndays)
            df_response = df_response[df_response["date"] >= date_limit]
        if df_response.shape[0] == 0:
            return []
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

def create_nested_mutation_query(location_id = None, lineages = [], mutations = []):
    # For multiple lineages and mutations: (Lineage 1 AND mutation 1 AND mutation 2..) OR (Lineage 2 AND mutation 1 AND mutation 2..) ...
    query_obj = {
        "bool": {
            "should": []
        }
    }
    bool_should = []
    for i in lineages:
        bool_must = {
            "bool": {
                "must": []
            }
        }
        bool_must["bool"]["must"].append({
            "term": {
                "pangolin_lineage": i
            }
        })
        bool_should.append(bool_must)
    bool_mutations = []
    for i in mutations:
        bool_mutations.append({
            "nested": {
                "path": "mutations",
                "query": {
                    "term" : { "mutations.mutation" : i }
                }
            }
        })
    if len(bool_mutations) > 0: # If mutations specified
        if len(bool_should) > 0: # If lineage and mutations specified
            for i in bool_should:
                i["bool"]["must"].extend(bool_mutations)
            query_obj["bool"]["should"] = bool_should
        else:                   # If only mutations are specified
            query_obj = {
                "bool": {
                    "must": bool_mutations
                }
            }
    else:                       # If only lineage specified
        query_obj["bool"]["should"] = bool_should
    parse_location_id_to_query(location_id, query_obj)
    return query_obj

def classify_other_category(grp, keep_lineages):
    grp.loc[(~grp["lineage"].isin(keep_lineages)) | (grp["lineage"] == "none"), "lineage"] = "other" # Temporarily remove none. TODO: Proper fix
    grp = grp.groupby("lineage").agg({
        "total_count": lambda x: x.iloc[0],
        "lineage_count": "sum"
    })
    return grp

def get_major_lineage_prevalence(df, index_col, keep_lineages = [], prevalence_threshold = 0.05, nday_threshold = 10, ndays = 180):
    date_limit = dt.today() - timedelta(days = ndays)
    lineages_to_retain = df[(df["prevalence"] >= prevalence_threshold) & (df["date"] >= date_limit)]["lineage"].value_counts()
    num_unique_dates = df[df["date"] >= date_limit]["date"].unique().shape[0]
    if num_unique_dates < nday_threshold:
        nday_threshold = round((nday_threshold/ndays) * num_unique_dates)
    lineages_to_retain = lineages_to_retain[lineages_to_retain >= nday_threshold].index.tolist()
    lineages_to_retain.extend(keep_lineages)
    df = df.groupby(index_col).apply(classify_other_category, lineages_to_retain)
    df = df.reset_index()
    df.loc[:,"prevalence"] = df["lineage_count"]/df["total_count"]
    return df

def parse_location_id_to_query(query_id, query_obj = None):
    if query_id == None:
        return None
    location_codes = query_id.split("_")
    if query_obj == None:
        query_obj = {
            "bool": {
                "must": []
            }
        }
    location_types = ["country_id", "division_id", "location_id"]
    for i in range(min(3, len(location_codes))):
        if i == 1 and len(location_codes[i].split("-")) > 1:              # For division remove iso2 code if present
            location_codes[i] = location_codes[i].split("-")[1]
        if "must" in query_obj["bool"]:
            query_obj["bool"]["must"].append({
                "term": {
                    location_types[i]: location_codes[i]
                }
            })
        elif "should" in query_obj["bool"] and len(query_obj["bool"]["should"]) > 0: # For create_nested_mutation_query IF both lineages and mutations supplied.
            for bool_must in query_obj["bool"]["should"]:
                bool_must["bool"]["must"].append({
                    "term": {
                        location_types[i]: location_codes[i]
                    }
                })
    return query_obj

def create_lineage_concat_query(queries, query_tmpl):
    queries = queries.split(",")
    if len(queries) == 1:
        query_tmpl["query"] = {
            "bool": {
                "filter": [
                    {"term": {"pangolin_lineage": queries[0]}}
                ]
            }
        }
    else:
        query_tmpl["query"] = {
            "bool": {
                "should": [
                    {"term": {"pangolin_lineage": i}}
                    for i in queries
                ]
            }
        }

def create_iterator(lineages, mutations):
    print(lineages)
    print(mutations)
    if len(lineages) > 0:
        return zip(lineages, [mutations] * len(lineages))
    if len(lineages) == 0 and len(mutations) > 0:
        return zip([None], [mutations])
    return zip([], [])
