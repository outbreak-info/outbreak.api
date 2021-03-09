from .lineage import LineageByCountryHandler, LineageByDivisionHandler, LineageAndCountryHandler, LineageAndDivisionHandler, LineageHandler, LineageMutationsHandler, MutationDetailsHandler, MutationsByLineage
from .prevalence import GlobalPrevalenceByTimeHandler, PrevalenceByLocationAndTimeHandler, CumulativePrevalenceByLocationHandler, PrevalenceAllLineagesByLocationHandler, PrevalenceByAAPositionHandler
from .general import LocationHandler, LocationDetailsHandler, MetadataHandler, MutationHandler, SubmissionLagHandler, SequenceCountHandler, MostRecentCollectionDateGlobalHandler, MostRecentCollectionDateByCountryHandler, MostRecentCollectionDateByDivisionHandler, MostRecentCollectionDateByCountyHandler, MostRecentSubmissionDateGlobalHandler, MostRecentSubmissionDateByCountryHandler, MostRecentSubmissionDateByDivisionHandler, MostRecentSubmissionDateByCountyHandler

routes = [
    (r"/genomics/lineage-by-country", LineageByCountryHandler),
    (r"/genomics/lineage-by-division", LineageByDivisionHandler),
    (r"/genomics/lineage-and-country", LineageAndCountryHandler),
    (r"/genomics/lineage-and-division", LineageAndDivisionHandler),
    (r"/genomics/sequence-count", SequenceCountHandler),
    (r"/genomics/global-prevalence", GlobalPrevalenceByTimeHandler),
    (r"/genomics/prevalence-by-location", PrevalenceByLocationAndTimeHandler),
    (r"/genomics/prevalence-by-location-all-lineages", PrevalenceAllLineagesByLocationHandler),
    (r"/genomics/prevalence-by-position", PrevalenceByAAPositionHandler),
    (r"/genomics/lineage-by-sub-admin-most-recent", CumulativePrevalenceByLocationHandler),
    (r"/genomics/most-recent-collection-date", MostRecentCollectionDateGlobalHandler),
    (r"/genomics/most-recent-collection-date-by-country", MostRecentCollectionDateByCountryHandler),
    (r"/genomics/most-recent-collection-date-by-division", MostRecentCollectionDateByDivisionHandler),
    (r"/genomics/most-recent-collection-date-by-county", MostRecentCollectionDateByCountyHandler),
    (r"/genomics/most-recent-submission-date", MostRecentSubmissionDateGlobalHandler),
    (r"/genomics/most-recent-submission-date-by-country", MostRecentSubmissionDateByCountryHandler),
    (r"/genomics/most-recent-submission-date-by-division", MostRecentSubmissionDateByDivisionHandler),
    (r"/genomics/most-recent-submission-date-by-county", MostRecentSubmissionDateByCountyHandler),
    (r"/genomics/mutation-details", MutationDetailsHandler),
    (r"/genomics/mutations-by-lineage", MutationsByLineage),
    (r"/genomics/lineage-mutations", LineageMutationsHandler),
    (r"/genomics/collection-submission", SubmissionLagHandler),
    (r"/genomics/lineage", LineageHandler),
    (r"/genomics/location", LocationHandler),
    (r"/genomics/location-lookup", LocationDetailsHandler),
    (r"/genomics/mutations", MutationHandler),
    (r"/genomics/metadata", MetadataHandler)
]
