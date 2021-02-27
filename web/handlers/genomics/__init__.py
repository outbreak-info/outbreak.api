from .lineage import LineageByCountryHandler, LineageByDivisionHandler, LineageAndCountryHandler, LineageAndDivisionHandler, LineageHandler, LineageMutationsHandler, MutationDetailsHandler, MutationsByLineage
from .prevalence import PrevalenceByLocationHandler, PrevalenceByCountryAndTimeHandler, PrevalenceByDivisionAndTimeHandler, PrevalenceHandler, PrevalenceAllLineagesByLocationHandler, PrevalenceByAAPositionHandler, PrevalenceByCountyAndTimeHandler
from .general import MostRecentCollectionDate, CountryHandler, DivisionHandler, MetadataHandler, MostRecentSubmissionDate, MutationHandler, SubmissionLagHandler

routes = [
    (r"/genomics/lineage-by-country", LineageByCountryHandler),
    (r"/genomics/lineage-by-division", LineageByDivisionHandler),
    (r"/genomics/lineage-and-country", LineageAndCountryHandler),
    (r"/genomics/lineage-and-division", LineageAndDivisionHandler),
    (r"/genomics/prevalence-by-location", PrevalenceByLocationHandler),
    (r"/genomics/prevalence-by-country-all-lineages", PrevalenceAllLineagesByLocationHandler),
    (r"/genomics/prevalence-by-division-all-lineages", PrevalenceAllLineagesByLocationHandler),
    (r"/genomics/prevalence-by-position", PrevalenceByAAPositionHandler),
    (r"/genomics/global-prevalence", PrevalenceHandler),
    (r"/genomics/lineage-by-country-most-recent", PrevalenceByCountryAndTimeHandler),
    (r"/genomics/lineage-by-division-most-recent", PrevalenceByDivisionAndTimeHandler),
    (r"/genomics/lineage-by-county-most-recent", PrevalenceByCountyAndTimeHandler),
    (r"/genomics/most-recent-collection-date", MostRecentCollectionDate),
    (r"/genomics/most-recent-submission-date", MostRecentSubmissionDate),
    (r"/genomics/mutation-details", MutationDetailsHandler),
    (r"/genomics/mutations-by-lineage", MutationsByLineage),
    (r"/genomics/lineage-mutations", LineageMutationsHandler),
    (r"/genomics/collection-submission", SubmissionLagHandler),
    (r"/genomics/country", CountryHandler),
    (r"/genomics/lineage", LineageHandler),
    (r"/genomics/division", DivisionHandler),
    (r"/genomics/mutations", MutationHandler),
    (r"/genomics/metadata", MetadataHandler)
]
