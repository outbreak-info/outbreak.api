from biothings.web.settings.default import APP_LIST

API_PREFIX = "genomics"
ES_INDEX = "outbreak-genomics"

APP_LIST = [
    (r"/{pre}/lineage-by-country", "web.handlers.genomics.lineage.LineageByCountryHandler"),
    (r"/{pre}/lineage-by-division", "web.handlers.genomics.LineageByDivisionHandler"),
    (r"/{pre}/lineage-and-country", "web.handlers.genomics.LineageAndCountryHandler"),
    (r"/{pre}/lineage-and-division", "web.handlers.genomics.LineageAndDivisionHandler"),
    (r"/{pre}/sequence-count", "web.handlers.genomics.SequenceCountHandler"),
    (r"/{pre}/global-prevalence", "web.handlers.genomics.GlobalPrevalenceByTimeHandler"),
    (r"/{pre}/prevalence-by-location", "web.handlers.genomics.PrevalenceByLocationAndTimeHandler"),
    (
        r"/{pre}/prevalence-by-location-all-lineages",
        "web.handlers.genomics.PrevalenceAllLineagesByLocationHandler",
    ),
    (r"/{pre}/prevalence-by-position", "web.handlers.genomics.PrevalenceByAAPositionHandler"),
    (
        r"/{pre}/lineage-by-sub-admin-most-recent",
        "web.handlers.genomics.CumulativePrevalenceByLocationHandler",
    ),
    (
        r"/{pre}/most-recent-collection-date-by-location",
        "web.handlers.genomics.MostRecentCollectionDateHandler",
    ),
    (
        r"/{pre}/most-recent-submission-date-by-location",
        "web.handlers.genomics.MostRecentSubmissionDateHandler",
    ),
    (r"/{pre}/mutation-details", "web.handlers.genomics.MutationDetailsHandler"),
    (r"/{pre}/mutations-by-lineage", "web.handlers.genomics.MutationsByLineage"),
    (r"/{pre}/lineage-mutations", "web.handlers.genomics.LineageMutationsHandler"),
    (r"/{pre}/collection-submission", "web.handlers.genomics.SubmissionLagHandler"),
    (r"/{pre}/lineage", "web.handlers.genomics.LineageHandler"),
    (r"/{pre}/location", "web.handlers.genomics.LocationHandler"),
    (r"/{pre}/location-lookup", "web.handlers.genomics.LocationDetailsHandler"),
    (r"/{pre}/mutations", "web.handlers.genomics.MutationHandler"),
    (r"/{pre}/metadata", "web.handlers.genomics.MetadataHandler"),
    (r"/{pre}/gisaid-id-lookup", "web.handlers.genomics.GisaidIDHandler"),
    (r"/{pre}/get-auth-token", "web.handlers.genomics.GISAIDTokenHandler"),
    *APP_LIST,
]
