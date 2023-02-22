from datetime import datetime as dt, timedelta

import pandas as pd

from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import (
    compute_rolling_mean_all_lineages,
    compute_total_count,
    create_date_range_filter,
    expand_dates,
    get_major_lineage_prevalence,
    parse_location_id_to_query,
    parse_time_window_to_query,
)


class PrevalenceAllLineagesByLocationHandler(BaseHandler):
    # size = 100  # If size=1000 it will raise too_many_buckets_exception in case missing location_id in query.
    name = "prevalence-by-location-all-lineages"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "location_id": {"type": str, "default": None},
        "window": {"type": int, "default": None, "min": 1},
        "other_threshold": {"type": float, "default": 0.05, "min": 0, "max": 1},
        "nday_threshold": {"type": int, "default": 10, "min": 1},
        "ndays": {"type": int, "default": 180, "min": 1},
        "other_exclude": {"type": str, "default": None},
        "cumulative": {"type": bool, "default": False},
        "min_date": {"type": str, "default": None, "date_format": "%Y-%m-%d"},
        "max_date": {"type": str, "default": None, "date_format": "%Y-%m-%d"},
    }

    async def _get(self):
        query_location = self.args.location_id
        query_window = self.args.window
        query_other_threshold = self.args.other_threshold
        query_nday_threshold = self.args.nday_threshold
        query_ndays = self.args.ndays
        query_other_exclude = self.args.other_exclude
        query_other_exclude = (
            query_other_exclude.split(",") if query_other_exclude is not None else []
        )
        query_cumulative = self.args.cumulative
        query = {
            "size": 0,
            "aggs": {
                "count": {
                    "terms": {"field": "date_collected", "size": self.size},
                    "aggs": {
                        "lineage_count": {"terms": {"field": "pangolin_lineage", "size": self.size}}
                    },
                }
            },
        }
        query_obj = parse_location_id_to_query(query_location)
        date_range_filter = create_date_range_filter(
            "date_collected", self.args.min_date, self.args.max_date
        )
        query_obj = parse_time_window_to_query(date_range_filter, query_obj=query_obj)
        if query_obj:
            query["query"] = query_obj
        # import json
        # print(json.dumps(query))
        resp = await self.asynchronous_fetch(query)
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
        if not flattened_response:
            return {"success": True, "results": []}
        df_response = (
            pd.DataFrame(flattened_response)
            .assign(
                date=lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"),
                prevalence=lambda x: x["lineage_count"] / x["total_count"],
            )
            .sort_values("date")
        )
        if (
            query_window is not None and not date_range_filter
        ):  # discard query_window if either max_date or min_date exists
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
                df_response.groupby("lineage", group_keys=True)
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
