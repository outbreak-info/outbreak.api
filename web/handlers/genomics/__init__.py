from .lineage import LineageByCountryHandler, LineageByDivisionHandler, LineageAndCountryHandler, LineageAndDivisionHandler, LineageHandler, LineageMutationsHandler, MutationDetailsHandler, MutationsByLineage
from .prevalence import PrevalenceByLocationHandler, CumulativeGlobalPrevalenceHandler, CumulativePrevalenceByCountryHandler, CumulativePrevalenceByDivisionHandler, PrevalenceHandler, PrevalenceAllLineagesByCountryHandler, PrevalenceAllLineagesByDivisionHandler, PrevalenceAllLineagesByCountyHandler, PrevalenceByAAPositionHandler
from .general import MostRecentCollectionDate, CountryHandler, DivisionHandler, CountyHandler, MetadataHandler, MostRecentSubmissionDate, MutationHandler, SubmissionLagHandler, SequenceCountHandler

routes = [
    (r"/genomics/lineage-by-country", LineageByCountryHandler),
    (r"/genomics/lineage-by-division", LineageByDivisionHandler),
    (r"/genomics/lineage-and-country", LineageAndCountryHandler),
    (r"/genomics/lineage-and-division", LineageAndDivisionHandler),
    (r"/genomics/sequence-count", SequenceCountHandler),
    (r"/genomics/prevalence-by-location", PrevalenceByLocationHandler),
    (r"/genomics/prevalence-by-country-all-lineages", PrevalenceAllLineagesByCountryHandler),
    (r"/genomics/prevalence-by-division-all-lineages", PrevalenceAllLineagesByDivisionHandler),
    (r"/genomics/prevalence-by-county-all-lineages", PrevalenceAllLineagesByCountyHandler),
    (r"/genomics/prevalence-by-position", PrevalenceByAAPositionHandler),
    (r"/genomics/global-prevalence", PrevalenceHandler),
    (r"/genomics/lineage-by-country-most-recent", CumulativeGlobalPrevalenceHandler),
    (r"/genomics/lineage-by-division-most-recent", CumulativePrevalenceByCountryHandler),
    (r"/genomics/lineage-by-county-most-recent", CumulativePrevalenceByDivisionHandler),
    (r"/genomics/most-recent-collection-date", MostRecentCollectionDate),
    (r"/genomics/most-recent-submission-date", MostRecentSubmissionDate),
    (r"/genomics/mutation-details", MutationDetailsHandler),
    (r"/genomics/mutations-by-lineage", MutationsByLineage),
    (r"/genomics/lineage-mutations", LineageMutationsHandler),
    (r"/genomics/collection-submission", SubmissionLagHandler),
    (r"/genomics/country", CountryHandler),
    (r"/genomics/lineage", LineageHandler),
    (r"/genomics/county", CountyHandler),
    (r"/genomics/division", DivisionHandler),
    (r"/genomics/mutations", MutationHandler),
    (r"/genomics/metadata", MetadataHandler)
]
