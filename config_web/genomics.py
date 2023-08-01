ES_INDEX = "outbreak-genomics"

ES_MUTLESS_INDEX = "genomics_api_local_mutless"
ES_MUTS_INDEX = "genomics_api_local_muts"
ES_INDEX_V3 = [ES_MUTLESS_INDEX, ES_MUTS_INDEX]

API_PREFIX = "genomics"
API_VERSION = "v2"

APP_LIST_V3 = [
    (
        r"/{pre}/v3/lineage-mutations",
        "web.handlers.v3.genomics.lineage_mutations.LineageMutationsHandler",
    ),
    (
        r"/{pre}/v3/lineage",
        "web.handlers.v3.genomics.lineage.LineageHandler",
    ),
    (
        r"/{pre}/v3/lineage-by-country",
        "web.handlers.v3.genomics.lineage_by_country.LineageByCountryHandler",
    ),
    (
        r"/{pre}/v3/mutations-by-lineage",
        "web.handlers.v3.genomics.mutations_by_lineage.MutationsByLineage",
    ),
    (
        r"/{pre}/v3/location-lookup",
        "web.handlers.v3.genomics.location_details.LocationDetailsHandler",
    ),
    (
        r"/{pre}/v3/mutation-details",
        "web.handlers.v3.genomics.mutation_details.MutationDetailsHandler",
    ),
    (
        r"/{pre}/v3/prevalence-by-location",
        "web.handlers.v3.genomics.PrevalenceByLocationAndTimeHandler",
    ),
    (
        r"/{pre}/v3/global-prevalence",
        "web.handlers.v3.genomics.GlobalPrevalenceByTimeHandler",
    ),
    (
        r"/{pre}/v3/sequence-count",
        "web.handlers.v3.genomics.SequenceCountHandler",
    ),
]

APP_LIST_V2 = [
    (
        r"/{pre}/{ver}/lineage-mutations",
        "web.handlers.v2.genomics.lineage_mutations.LineageMutationsHandler",
    ),
    (r"/{pre}/{ver}/lineage", "web.handlers.v2.genomics.LineageHandler"),
    (r"/{pre}/{ver}/location", "web.handlers.v2.genomics.LocationHandler"),
    (
        r"/{pre}/{ver}/prevalence-by-location",
        "web.handlers.v2.genomics.PrevalenceByLocationAndTimeHandler",
    ),
    (
        r"/{pre}/{ver}/prevalence-by-location-all-lineages",
        "web.handlers.v2.genomics.PrevalenceAllLineagesByLocationHandler",
    ),
    (
        r"/{pre}/{ver}/prevalence-by-position",
        "web.handlers.v2.genomics.PrevalenceByAAPositionHandler",
    ),
    (
        r"/{pre}/{ver}/mutation-details",
        "web.handlers.v2.genomics.MutationDetailsHandler",
    ),
    (
        r"/{pre}/{ver}/collection-submission",
        "web.handlers.v2.genomics.SubmissionLagHandler",
    ),
    (
        r"/{pre}/{ver}/mutations",
        "web.handlers.v2.genomics.MutationHandler",
    ),
    (
        r"/{pre}/{ver}/mutations-by-lineage",
        "web.handlers.v2.genomics.MutationsByLineage",
    ),
    (
        r"/{pre}/{ver}/location-lookup",
        "web.handlers.v2.genomics.LocationDetailsHandler",
    ),
    (
        r"/{pre}/{ver}/most-recent-collection-date-by-location",
        "web.handlers.v2.genomics.MostRecentCollectionDateHandler",
    ),
    (
        r"/{pre}/{ver}/most-recent-submission-date-by-location",
        "web.handlers.v2.genomics.MostRecentSubmissionDateHandler",
    ),
    (
        r"/{pre}/{ver}/sequence-count",
        "web.handlers.v2.genomics.SequenceCountHandler",
    ),
    (
        r"/{pre}/{ver}/lineage-by-sub-admin-most-recent",
        "web.handlers.v2.genomics.CumulativePrevalenceByLocationHandler",
    ),
]

APP_LIST_SWITCHED_TO_V2 = [
    (
        r"/{pre}/lineage-mutations",
        "web.handlers.v2.genomics.lineage_mutations.LineageMutationsHandler",
    ),
    (r"/{pre}/lineage", "web.handlers.v2.genomics.LineageHandler"),
    (r"/{pre}/location", "web.handlers.v2.genomics.LocationHandler"),
    (
        r"/{pre}/prevalence-by-location",
        "web.handlers.v2.genomics.PrevalenceByLocationAndTimeHandler",
    ),
    (
        r"/{pre}/prevalence-by-location-all-lineages",
        "web.handlers.v2.genomics.PrevalenceAllLineagesByLocationHandler",
    ),
]

APP_LIST_v1 = [
    (r"/{pre}/v1/lineage-mutations", "web.handlers.genomics.LineageMutationsHandler"),
    (r"/{pre}/v1/lineage", "web.handlers.genomics.LineageHandler"),
    (r"/{pre}/v1/location", "web.handlers.genomics.LocationHandler"),
    (
        r"/{pre}/v1/prevalence-by-location",
        "web.handlers.genomics.PrevalenceByLocationAndTimeHandler",
    ),
    (
        r"/{pre}/v1/prevalence-by-location-all-lineages",
        "web.handlers.genomics.PrevalenceAllLineagesByLocationHandler",
    ),
]

APP_LIST_ORIGIN = [
    (r"/{pre}/lineage-by-country", "web.handlers.genomics.lineage.LineageByCountryHandler"),
    (r"/{pre}/lineage-by-division", "web.handlers.genomics.LineageByDivisionHandler"),
    (r"/{pre}/lineage-and-country", "web.handlers.genomics.LineageAndCountryHandler"),
    (r"/{pre}/lineage-and-division", "web.handlers.genomics.LineageAndDivisionHandler"),
    (r"/{pre}/sequence-count", "web.handlers.genomics.SequenceCountHandler"),
    (r"/{pre}/global-prevalence", "web.handlers.genomics.GlobalPrevalenceByTimeHandler"),
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
    (r"/{pre}/collection-submission", "web.handlers.genomics.SubmissionLagHandler"),
    (r"/{pre}/location-lookup", "web.handlers.genomics.LocationDetailsHandler"),
    (r"/{pre}/mutations", "web.handlers.genomics.MutationHandler"),
    (r"/{pre}/metadata", "web.handlers.genomics.MetadataHandler"),
    (r"/{pre}/gisaid-id-lookup", "web.handlers.genomics.GisaidIDHandler"),
    (r"/{pre}/get-auth-token", "web.handlers.genomics.GISAIDTokenHandler"),
]

APP_LIST = [
    *APP_LIST_V3,
    *APP_LIST_SWITCHED_TO_V2,
    *APP_LIST_V2,
    *APP_LIST_v1,
    *APP_LIST_ORIGIN,
]
