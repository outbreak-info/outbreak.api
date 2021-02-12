from .lineage import LineageByCountryHandler, LineageByDivisionHandler, LineageAndCountryHandler, LineageAndDivisionHandler, LineageHandler, LineageMutationsHandler
from .prevalence import PrevalenceByLocationHandler, PrevalenceByCountryAndTimeHandler, PrevalenceByDivisionAndTimeHandler, PrevalenceHandler, PrevalenceAllLineagesByCountryHandler, PrevalenceAllLineagesByDivisionHandler
from .general import MostRecentCollectionDate, CountryHandler, DivisionHandler, MetadataHandler, MostRecentSubmissionDate, MutationHandler

routes = [
    (r"/genomics/lineage-by-country", LineageByCountryHandler),
    (r"/genomics/lineage-by-division", LineageByDivisionHandler),
    (r"/genomics/lineage-and-country", LineageAndCountryHandler),
    (r"/genomics/lineage-and-division", LineageAndDivisionHandler),
    (r"/genomics/prevalence-by-location", PrevalenceByLocationHandler),
    (r"/genomics/prevalence-by-country-all-lineages", PrevalenceAllLineagesByCountryHandler),
    (r"/genomics/prevalence-by-division-all-lineages", PrevalenceAllLineagesByDivisionHandler),
    (r"/genomics/global-prevalence", PrevalenceHandler),
    (r"/genomics/lineage-by-country-most-recent", PrevalenceByCountryAndTimeHandler),
    (r"/genomics/lineage-by-division-most-recent", PrevalenceByDivisionAndTimeHandler),
    (r"/genomics/most-recent-collection-date", MostRecentCollectionDate),
    (r"/genomics/most-recent-submission-date", MostRecentSubmissionDate),
    (r"/genomics/country", CountryHandler),
    (r"/genomics/lineage", LineageHandler),
    (r"/genomics/division", DivisionHandler),
    (r"/genomics/lineage-mutations", LineageMutationsHandler),
    (r"/genomics/mutations", MutationHandler),
    (r"/genomics/metadata", MetadataHandler)
]
