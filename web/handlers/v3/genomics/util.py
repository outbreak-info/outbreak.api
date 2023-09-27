from datetime import datetime as dt, timedelta

import pandas as pd

# Third-party imports
from scipy.stats import beta


def get_total_hits(d):  # To account for difference in ES versions 7.12.0 vs 6.8.13
    return (
        d["hits"]["total"]["value"] if isinstance(d["hits"]["total"], dict) else d["hits"]["total"]
    )


def calculate_proportion(_x, _n):
    x = _x.round()
    n = _n.round()
    ci_low, ci_upp = beta.interval(1 - 0.05, x + 0.5, n - x + 0.5)  # Jeffreys Interval
    est_proportion = _x / _n
    return est_proportion, ci_low, ci_upp


def escape_special_characters(query_string):
    # List of characters to escape and their replacements
    special_characters = {
        "\\": "\\\\",
        ":": "\\:",
        "/": "\\/",
    }

    # Replace special characters in the query string
    for char, replacement in special_characters.items():
        query_string = query_string.replace(char, replacement)

    return query_string


# TODO: Improve this function
def create_query_filter(lineages="", mutations="", locations=""):
    filters = []
    if lineages and len(lineages) > 0:
        lineages = "pangolin_lineage: ({})".format(lineages)
        filters.append(lineages)
    if mutations and len(mutations) > 0:
        mutations = escape_special_characters(mutations)
        mutations = "mutations: ({})".format(mutations)
        filters.append(mutations)
    query_filters = " AND ".join(filters)

    if not lineages and not mutations and not locations:
        query_filters = "*"
    return query_filters


# TODO: Improve this function
def create_query_filter_key(lineages="", mutations="", locations=""):
    filters = []
    if lineages and len(lineages) > 0 and mutations and len(mutations) > 0:
        lineages = "({})".format(lineages)
        filters.append(lineages)
        mutations = "({})".format(mutations)
        filters.append(mutations)
    else:
        if lineages and len(lineages) > 0:
            lineages = "{}".format(lineages)
            filters.append(lineages)
        if mutations and len(mutations) > 0:
            mutations = "{}".format(mutations)
            filters.append(mutations)
    query_filters = " AND ".join(filters)

    if not lineages and not mutations and not locations:
        query_filters = "*"
    return query_filters


def parse_location_id_to_query(query_id, query_obj=None):
    if query_id == None:
        return None
    location_codes = query_id.split("_")
    if query_obj == None:
        query_obj = {"bool": {"must": []}}
    location_types = ["country_id", "division_id", "location_id"]
    for i in range(min(3, len(location_codes))):
        if (
            i == 1 and len(location_codes[i].split("-")) > 1
        ):  # For division remove iso2 code if present
            location_codes[i] = location_codes[i].split("-")[1]
        if "must" in query_obj["bool"]:
            query_obj["bool"]["must"].append({"term": {location_types[i]: location_codes[i]}})
        elif (
            "should" in query_obj["bool"] and len(query_obj["bool"]["should"]) > 0
        ):  # For create_nested_mutation_query IF both lineages and mutations supplied.
            for bool_must in query_obj["bool"]["should"]:
                bool_must["bool"]["must"].append({"term": {location_types[i]: location_codes[i]}})
    return query_obj


def compute_rolling_mean(df, index_col, col, new_col):
    df = (
        df.set_index(index_col)
        .assign(**{new_col: lambda x: x[col].rolling("7d").mean()})
        .reset_index()
    )
    return df


def transform_prevalence(resp, path_to_results=None, cumulative=False):
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    if len(buckets) == 0:
        return {"success": True, "results": {}}
    flattened_response = [
        {
            "date": i["key"],
            "total_count": i["doc_count"],
            "lineage_count": i["lineage_count"]["doc_count"],
        }
        for i in buckets
        if len(i["key"].split("-")) > 1 and "XX" not in i["key"]
    ]
    df_response = (
        pd.DataFrame(flattened_response)
        .assign(date=lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
        .sort_values("date")
    )
    first_date = df_response[df_response["lineage_count"] > 0]["date"].min()
    dict_response = {}
    if not cumulative:
        df_response = df_response[
            df_response["date"] >= first_date - pd.to_timedelta(6, unit="d")
        ]  # Go back 6 days for total_rolling
        df_response = compute_rolling_mean(
            df_response, "date", "total_count", "total_count_rolling"
        )
        df_response = compute_rolling_mean(
            df_response, "date", "lineage_count", "lineage_count_rolling"
        )
        df_response = df_response[
            df_response["date"] >= first_date
        ]  # Revert back to first date after total_rolling calculations are complete
        d = calculate_proportion(
            df_response["lineage_count_rolling"], df_response["total_count_rolling"]
        )
        df_response.loc[:, "proportion"] = d[0]
        df_response.loc[:, "proportion_ci_lower"] = d[1]
        df_response.loc[:, "proportion_ci_upper"] = d[2]
        df_response.loc[:, "date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        dict_response = df_response.to_dict(orient="records")
    else:  # For cumulative only calculate cumsum prevalence
        df_response = df_response[df_response["date"] >= first_date]
        if df_response.shape[0] == 0:
            dict_response = {
                "global_prevalence": 0,
                "total_count": 0,
                "lineage_count": 0,
                "first_detected": None,
                "last_detected": None,
            }
        else:
            lineage_cumsum = int(df_response["lineage_count"].sum())
            total_cumsum = int(df_response["total_count"].sum())
            df_date_sorted = df_response[df_response["lineage_count"] > 0].sort_values("date")
            dict_response = {
                "global_prevalence": lineage_cumsum / total_cumsum,
                "total_count": total_cumsum,
                "lineage_count": lineage_cumsum,
                "first_detected": df_date_sorted["date"].iloc[0].strftime("%Y-%m-%d"),
                "last_detected": df_date_sorted["date"].iloc[-1].strftime("%Y-%m-%d"),
            }
    return dict_response


def create_iterator(lineages, mutations):
    if lineages is not None and len(lineages) > 0:
        return zip(range(len(lineages)), lineages, [mutations] * len(lineages))
    if lineages is not None and len(lineages) == 0 and mutations is not None and len(mutations) > 0:
        return zip([0], [None], [mutations])
    return zip([], [], [])


def create_iterator_q(q_list):
    if q_list is not None and len(q_list) > 0:
        return zip(range(len(q_list)), q_list)
    if q_list is not None and len(q_list) == 0:
        return zip([0], [None])
    return zip([], [])


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


def transform_prevalence_by_location_and_time(flattened_response, ndays=None, query_detected=False):
    df_response = (
        pd.DataFrame(flattened_response)
        .assign(date=lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))
        .sort_values("date")
    )
    dict_response = {}
    if not query_detected:
        if ndays is not None:
            date_limit = dt.today() - timedelta(days=ndays)
            df_response = df_response[df_response["date"] >= date_limit]
        if df_response.shape[0] == 0:
            return []
        df_response = df_response.groupby("name").apply(
            compute_cumulative, ["total_count", "lineage_count"]
        )
        df_response.loc[:, "date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
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
