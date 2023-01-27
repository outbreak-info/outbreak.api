from datetime import datetime as dt, timedelta

import pandas as pd
from tornado import gen

from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import (
    compute_rolling_mean_all_lineages,
    compute_total_count,
    expand_dates,
    get_major_lineage_prevalence,
    parse_location_id_to_query,
)


class PrevalenceAllLineagesByLocationHandler(BaseHandler):
    @gen.coroutine
    def _get(self):
        query_location = self.get_argument("location_id", None)
        query_window = self.get_argument("window", None)
        query_window = int(query_window) if query_window is not None else None
        query_other_threshold = self.get_argument("other_threshold", 0.05)
        query_other_threshold = float(query_other_threshold)
        query_nday_threshold = self.get_argument("nday_threshold", 10)
        query_nday_threshold = float(query_nday_threshold)
        query_ndays = self.get_argument("ndays", 180)
        query_ndays = int(query_ndays)
        query_other_exclude = self.get_argument("other_exclude", None)
        query_other_exclude = (
            query_other_exclude.split(",") if query_other_exclude is not None else []
        )
        query_cumulative = self.get_argument("cumulative", None)
        query_cumulative = True if query_cumulative == "true" else False
        query = {
            "size": 0,
            "query": {},
            "aggs": {
                "count": {
                    "terms": {"field": "date_collected", "size": self.size},
                    "aggs": {
                        "lineage_count": {"terms": {"field": "pangolin_lineage", "size": self.size}}
                    },
                }
            },
        }
        query["query"] = parse_location_id_to_query(query_location)
        resp = yield self.asynchronous_fetch(query)
        buckets = resp
        path_to_results = ["aggregations", "count", "buckets"]
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = []
        for i in buckets:
            if len(i["key"].split("-")) == 1 or "XX" in i["key"]:
                continue
            for j in i["lineage_count"]["buckets"]:
                flattened_response.append(
                    {
                        "date": i["key"],
                        "total_count": i["doc_count"],
                        "lineage_count": j["doc_count"],
                        "lineage": j["key"],
                    }
                )
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(
                date=lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"),
                prevalence=lambda x: x["lineage_count"] / x["total_count"],
            )
            .sort_values("date")
        )
        if query_window is not None:
            df_response = df_response[
                df_response["date"] >= (dt.now() - timedelta(days=query_window))
            ]
        df_response = get_major_lineage_prevalence(
            df_response,
            "date",
            query_other_exclude,
            query_other_threshold,
            query_nday_threshold,
            query_ndays,
        )
        if not query_cumulative:
            df_response = (
                df_response.groupby("lineage")
                .apply(
                    compute_rolling_mean_all_lineages,
                    "date",
                    "lineage_count",
                    "lineage_count_rolling",
                    "lineage",
                )
                .reset_index()
            )
            df_response = df_response.groupby("date").apply(
                compute_total_count, "lineage_count_rolling", "total_count_rolling"
            )
            df_response.loc[:, "prevalence_rolling"] = (
                df_response["lineage_count_rolling"] / df_response["total_count_rolling"]
            )
            df_response.loc[
                df_response["prevalence_rolling"].isna(), "prevalence_rolling"
            ] = 0  # Prevalence is 0 if total_count_rolling == 0.
            df_response.loc[:, "date"] = df_response["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
            df_response = df_response.fillna("None")
            df_response = df_response[
                [
                    "date",
                    "total_count",
                    "lineage_count",
                    "lineage",
                    "prevalence",
                    "prevalence_rolling",
                ]
            ]
        else:
            df_response = (
                df_response.groupby("lineage")
                .apply(
                    expand_dates,
                    df_response["date"].min(),
                    df_response["date"].max(),
                    "date",
                    "lineage",
                )
                .reset_index()
            )
            df_response = (
                df_response.groupby("date")
                .apply(compute_total_count, "lineage_count", "total_count")
                .reset_index()
            )
            df_response = (
                df_response.groupby("lineage")
                .agg({"total_count": "sum", "lineage_count": "sum"})
                .reset_index()
            )
            df_response.loc[:, "prevalence"] = (
                df_response["lineage_count"] / df_response["total_count"]
            )
        resp = {"success": True, "results": df_response.to_dict(orient="records")}
        return resp
