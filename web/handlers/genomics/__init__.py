from .lineage import LineageByCountryHandler, LineageByDivisionHandler, LineageAndCountryHandler, LineageAndDivisionHandler, LineageHandler, LineageMutationsHandler, MutationDetailsHandler, MutationsByLineage
from .prevalence import GlobalPrevalenceByTimeHandler, PrevalenceByLocationAndTimeHandler, PrevalenceByLocationAndTimeHandler2, CumulativePrevalenceByLocationHandler, PrevalenceAllLineagesByLocationHandler, PrevalenceByAAPositionHandler
from .general import LocationHandler, LocationDetailsHandler, MetadataHandler, MutationHandler, SubmissionLagHandler, SequenceCountHandler, MostRecentSubmissionDateHandler, MostRecentCollectionDateHandler, GisaidIDHandler
from .gisaid_auth import GISAIDTokenHandler

routes = [
    (r"/genomics/lineage-by-country", LineageByCountryHandler),
    (r"/genomics/lineage-by-division", LineageByDivisionHandler),
    (r"/genomics/lineage-and-country", LineageAndCountryHandler),
    (r"/genomics/lineage-and-division", LineageAndDivisionHandler),
    (r"/genomics/sequence-count", SequenceCountHandler),
    (r"/genomics/global-prevalence", GlobalPrevalenceByTimeHandler),
    (r"/genomics/prevalence-by-location", PrevalenceByLocationAndTimeHandler),
    (r"/genomics/prevalence-by-location2", PrevalenceByLocationAndTimeHandler2),
    (r"/genomics/prevalence-by-location-all-lineages", PrevalenceAllLineagesByLocationHandler),
    (r"/genomics/prevalence-by-position", PrevalenceByAAPositionHandler),
    (r"/genomics/lineage-by-sub-admin-most-recent", CumulativePrevalenceByLocationHandler),
    (r"/genomics/most-recent-collection-date-by-location", MostRecentCollectionDateHandler),
    (r"/genomics/most-recent-submission-date-by-location", MostRecentSubmissionDateHandler),
    (r"/genomics/mutation-details", MutationDetailsHandler),
    (r"/genomics/mutations-by-lineage", MutationsByLineage),
    (r"/genomics/lineage-mutations", LineageMutationsHandler),
    (r"/genomics/collection-submission", SubmissionLagHandler),
    (r"/genomics/lineage", LineageHandler),
    (r"/genomics/location", LocationHandler),
    (r"/genomics/location-lookup", LocationDetailsHandler),
    (r"/genomics/mutations", MutationHandler),
    (r"/genomics/metadata", MetadataHandler),
    (r"/genomics/gisaid-id-lookup", GisaidIDHandler),
    (r"/genomics/get-auth-token", GISAIDTokenHandler)
]
